package org.pytorch.demo.objectdetection

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.drawable.BitmapDrawable
import android.os.Bundle
import android.os.PersistableBundle
import android.util.Log
import android.view.TextureView
import android.widget.TextView
import android.widget.Toast
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
import org.opencv.core.CvType
import org.opencv.core.Mat
import org.opencv.core.Point
import org.opencv.core.Scalar
import org.opencv.imgproc.Imgproc
import org.pytorch.demo.objectdetection.AbstractCameraXActivity.Companion
import java.nio.ByteBuffer

class CableDetectionActivity: AppCompatActivity() {
    private lateinit var previewView: PreviewView
    private val lines = mutableListOf<Pair<Point, Point>>()

    override fun onCreate(savedInstanceState: Bundle?,) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cable_detection)
        previewView  = findViewById(R.id.cablePreview)

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

            lines.clear()//make sure it doesn't overflow the memory
            val buffer: ByteBuffer = imageProxy.planes[0].buffer
            val data = ByteArray(buffer.capacity())
            buffer.get(data)

            val width = imageProxy.width
            val height = imageProxy.height
            val mat = Mat(height + height / 2, width, CvType.CV_8UC1)
            mat.put(0, 0, data)

            val grayMat = Mat()
            Imgproc.cvtColor(mat, grayMat, Imgproc.COLOR_YUV2GRAY_420)

            val edges = Mat()
            Imgproc.Canny(grayMat, edges, 50.0, 150.0)

            val linesMat = Mat()
            Imgproc.HoughLinesP(edges, linesMat, 1.0, Math.PI / 180, 50, 50.0, 10.0)

            for (i in 0 until linesMat.rows()) {
                val line = linesMat[i, 0]
                val pt1 = Point(line[0], line[1])
                val pt2 = Point(line[2], line[3])
                // Convert points to match the preview view's coordinate system
                val convertedPt1 = convertPoint(pt1, width, height)
                val convertedPt2 = convertPoint(pt2, width, height)

                lines.add(Pair(pt1, pt2))
            }
            //Debug
            Log.i("LineCount",lines.size.toString())

            runOnUiThread {
                // Draw lines on the preview
//                val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
//                val canvas = Canvas(bitmap)
//                val paint = Paint().apply {
//                    color = Color.RED
//                    strokeWidth = 20f
//                }
//                lines.forEach { line ->
//                    canvas.drawLine(
//                        line.first.x.toFloat(), line.first.y.toFloat(),
//                        line.second.x.toFloat(), line.second.y.toFloat(),
//                        paint
//                    )
//                }
//                previewView.overlay.clear()
//                previewView.overlay.add(BitmapDrawable(resources, bitmap))
                previewView.invalidate()
                drawLinesOnPreviewView(width, height)
            }
            //handle release of memory
            mat.release()
            grayMat.release()
            edges.release()
            linesMat.release()
        } finally {
            imageProxy.close()

        }

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
    }

    companion object {
        private const val REQUEST_CODE_CAMERA_PERMISSION = 101
        private val PERMISSIONS = arrayOf(Manifest.permission.CAMERA)
    }

}