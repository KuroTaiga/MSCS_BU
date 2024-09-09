package org.pytorch.demo.objectdetection

import android.Manifest
import android.content.DialogInterface
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.drawable.BitmapDrawable
import android.os.Bundle
import android.os.PersistableBundle
import android.provider.MediaStore
import android.util.Log
import android.view.TextureView
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import org.pytorch.Module
import org.opencv.android.OpenCVLoader
import org.opencv.core.Core
import org.opencv.core.CvType
import org.opencv.core.Mat
import org.opencv.core.Point
import org.opencv.core.Scalar
import org.opencv.imgproc.Imgproc
import org.opencv.video.Video
import org.pytorch.demo.objectdetection.AbstractCameraXActivity.Companion
import java.nio.ByteBuffer

class CableDetectionActivity: AppCompatActivity() {
    private val MIN_DISTANCE_THRESHOLD = 20.0
    private lateinit var previewView: PreviewView
    private lateinit var cableTextView: TextView
    private lateinit var cableOverlayView: CableOverlayView
    private var previousFrame: Mat? = null
    private val lines = mutableListOf<Pair<Point, Point>>()
    private var previousLineLengths = mutableListOf<Double>()
    override fun onCreate(savedInstanceState: Bundle?,) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cable_detection)
        previewView  = findViewById(R.id.cablePreview)
        cableTextView = findViewById(R.id.cableText)
        cableOverlayView = findViewById(R.id.cableOverlay)

        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                PERMISSIONS,
                REQUEST_CODE_CAMERA_PERMISSION
            )
        }
        startCamera()
        if (OpenCVLoader.initLocal()) {
            Log.i("OpenCV", "OpenCV loaded successfully");
        } else {
            Log.e("OpenCV", "OpenCV initialization failed!");
            (Toast.makeText(this, "OpenCV initialization failed!", Toast.LENGTH_LONG)).show();
            return;
        }
        val buttonSelect = findViewById<Button>(R.id.selectButton)
        buttonSelect.setOnClickListener(object : View.OnClickListener {
            override fun onClick(v: View) {
                previewView.setVisibility(View.INVISIBLE)

                val options = arrayOf<CharSequence>("Choose from Videos", "Take Video", "Cancel")
                val builder = AlertDialog.Builder(this@CableDetectionActivity)
                builder.setTitle("New Test Video")

                builder.setItems(options, object : DialogInterface.OnClickListener {
                    override fun onClick(dialog: DialogInterface, item: Int) {
                        if ((options[item] == "Take Video")) {
                            val takeVideo = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
                            startActivityForResult(takeVideo, 0)
                        } else if ((options[item] == "Choose from Videos")) {
                            val pickVideo = Intent(
                                Intent.ACTION_PICK,
                                MediaStore.Images.Media.INTERNAL_CONTENT_URI
                            )
                            startActivityForResult(pickVideo, 1)
                        } else if ((options[item] == "Cancel")) {
                            dialog.dismiss()
                        }
                    }
                })
                builder.show()
            }
        })
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == CableDetectionActivity.REQUEST_CODE_CAMERA_PERMISSION) {
            if (grantResults[0] == PackageManager.PERMISSION_DENIED) {
                Toast.makeText(
                    this,
                    "You can't use object detection example without granting CAMERA permission",
                    Toast.LENGTH_LONG
                )
                    .show()
                finish()
            } else {
                startCamera()
            }
        }
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
        cameraProviderFuture.addListener(Runnable {
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

            val preview = androidx.camera.core.Preview.Builder().build().also {
                it.setSurfaceProvider(previewView.surfaceProvider)
            }

            val imageAnalyzer = ImageAnalysis.Builder().build().also {
                it.setAnalyzer(ContextCompat.getMainExecutor(this)) { imageProxy ->
                    processImage(imageProxy)
                }
            }

            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview, imageAnalyzer
                )
            } catch (exc: Exception) {
                // Handle exception
                Log.e("CableCamera","Error with binding to life cycle")
            }

        }, ContextCompat.getMainExecutor(this))
    }

    private fun processImage(imageProxy: ImageProxy) {
        try {
            lines.clear() // Make sure it doesn't overflow the memory
            val currentLineLengths = mutableListOf<Double>()
            val buffer: ByteBuffer = imageProxy.planes[0].buffer
            val data = ByteArray(buffer.capacity())
            buffer.get(data)

            val width = imageProxy.width
            val height = imageProxy.height
            val mat = Mat(height + height / 2, width, CvType.CV_8UC1)
            mat.put(0, 0, data)

            val grayMat = Mat()
            Imgproc.cvtColor(mat, grayMat, Imgproc.COLOR_YUV2GRAY_420)

            if (previousFrame != null) {
                // Calculate Optical Flow
                val flow = Mat()

                Video.calcOpticalFlowFarneback(previousFrame, grayMat, flow, 0.5, 3, 15, 3, 5, 1.2, 0)

                // Calculate magnitude of flow
                val flowParts = ArrayList<Mat>(2)
                Core.split(flow, flowParts)
                val magnitude = Mat()
                val angle = Mat()
                Core.cartToPolar(flowParts[0], flowParts[1], magnitude, angle)

                // Threshold the magnitude
                val thresholded = Mat()
                Core.compare(magnitude, Scalar(10.0), thresholded, Core.CMP_GT)

                // Only detect lines in the regions with flow magnitude > 10.0
                val edges = Mat()
                Imgproc.Canny(grayMat, edges, 50.0, 150.0)
                Core.bitwise_and(edges, thresholded, edges)

                val linesMat = Mat()
                Imgproc.HoughLinesP(edges, linesMat, 1.0, Math.PI / 180, 50, 50.0, 10.0)

                val filteredLines = mutableListOf<Pair<Point,Point>>()

                for (i in 0 until linesMat.rows()) {
                    val line = linesMat[i, 0]
                    val pt1 = Point(line[0], line[1])
                    val pt2 = Point(line[2], line[3])
                    val lineLength = calculateLineLength(pt1, pt2)

                    // Store the line length for comparison in the next frame
                    currentLineLengths.add(lineLength)


                    if (previousLineLengths.isEmpty() || isLengthChangeAcceptable(lineLength, i)) {
                        // Convert points to match the preview view's coordinate system

                        val isFarEnough = filteredLines.all { existingLine ->
                            val midPoint1 = midpoint(existingLine.first, existingLine.second)
                            val midPoint2 = midpoint(pt1, pt2)
                            calculateLineLength(midPoint1, midPoint2) > MIN_DISTANCE_THRESHOLD
                        }
                        if (isFarEnough){
                            val convertedPt1 = convertPoint(pt1, width, height)
                            val convertedPt2 = convertPoint(pt2, width, height)
                            val linePair = Pair(convertedPt1, convertedPt2) as Pair<Point, Point>
                            lines.add(linePair)
                            filteredLines.add(linePair)
                        }
                    }
                }

                // Release Mats
                flow.release()
                magnitude.release()
                angle.release()
                thresholded.release()
                edges.release()
                linesMat.release()
            }
            previousLineLengths = currentLineLengths
            // Set the current frame as the previous frame for the next iteration
            previousFrame = grayMat.clone()

            // Update UI with detected lines
            runOnUiThread {
                drawLinesOnPreviewView(width, height)
                cableTextView.text = "Lines Detected: " + lines.size
            }

        } finally {
            imageProxy.close()
        }
    }

    private fun midpoint(pt1: Point, pt2: Point): Point {
        return Point((pt1.x + pt2.x) / 2, (pt1.y + pt2.y) / 2)
    }


    private fun calculateLineLength(pt1: Point, pt2: Point): Double {
        return Math.sqrt(Math.pow(pt2.x - pt1.x, 2.0) + Math.pow(pt2.y - pt1.y, 2.0))
    }

    private fun isLengthChangeAcceptable(currentLength: Double, index: Int): Boolean {
        if (index >= previousLineLengths.size) {
            return true
        }
        val previousLength = previousLineLengths[index]
        val lengthChangeThreshold = 5.0 // Define a threshold for acceptable length change

        return Math.abs(currentLength - previousLength) <= lengthChangeThreshold
    }


    private fun convertPoint(pt: Point, frameWidth: Int, frameHeight: Int): Any {
        // Convert the points from OpenCV coordinates to PreviewView coordinates
        val viewWidth = previewView.width
        val viewHeight = previewView.height

        // Depending on your camera feed's orientation and aspect ratio, adjust these mappings
        val xScale = viewWidth.toDouble() / frameWidth
        val yScale = viewHeight.toDouble() / frameHeight

        val x = pt.x * xScale
        val y = pt.y * yScale
        return Point(x, y)
    }
    private fun drawLinesOnPreviewView(frameWidth: Int, frameHeight: Int) {
        cableOverlayView.lines = lines.toList()
        cableOverlayView.invalidate()
        // Create a bitmap matching the preview view size
        val bitmap = Bitmap.createBitmap(previewView.width, previewView.height, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bitmap)
        val paint = Paint().apply {
            color = Color.RED
            strokeWidth = 5f
        }

        // Draw each line onto the bitmap
        lines.forEach { line ->
            canvas.drawLine(
                line.first.x.toFloat(), line.first.y.toFloat(),
                line.second.x.toFloat(), line.second.y.toFloat(),
                paint
            )
        }

        // Clear the previous overlay and add the new one
        previewView.overlay.clear()
        previewView.overlay.add(BitmapDrawable(resources, bitmap))
        previewView.invalidate()
    }

    companion object {
        private const val REQUEST_CODE_CAMERA_PERMISSION = 101
        private val PERMISSIONS = arrayOf(Manifest.permission.CAMERA)
    }

}