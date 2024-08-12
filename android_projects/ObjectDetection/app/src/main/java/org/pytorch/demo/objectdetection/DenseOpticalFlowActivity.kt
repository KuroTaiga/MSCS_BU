package org.pytorch.demo.objectdetection

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.drawable.BitmapDrawable
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import org.opencv.android.OpenCVLoader
import org.opencv.core.CvType
import org.opencv.core.Mat
import org.opencv.core.Point
import org.opencv.core.Scalar
import org.opencv.imgproc.Imgproc
import org.opencv.video.Video
import java.nio.ByteBuffer

class DenseOpticalFlowActivity : AppCompatActivity() {
    private lateinit var previewView: PreviewView
    private var prevGray: Mat? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dense_optical_flow)
        previewView = findViewById(R.id.denseOpticalFlowPreview)

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                PERMISSIONS,
                REQUEST_CODE_CAMERA_PERMISSION
            )
        }
        startCamera()
        if (OpenCVLoader.initDebug()) {
            Log.i("OpenCV", "OpenCV loaded successfully")
        } else {
            Log.e("OpenCV", "OpenCV initialization failed!")
            Toast.makeText(this, "OpenCV initialization failed!", Toast.LENGTH_LONG).show()
            return
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_CODE_CAMERA_PERMISSION) {
            if (grantResults[0] == PackageManager.PERMISSION_DENIED) {
                Toast.makeText(
                    this,
                    "You can't use this example without granting CAMERA permission",
                    Toast.LENGTH_LONG
                ).show()
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
                Log.e("DenseOpticalFlowActivity", "Error with binding to life cycle")
            }

        }, ContextCompat.getMainExecutor(this))
    }

    private fun processImage(imageProxy: ImageProxy) {
        try {
            val buffer: ByteBuffer = imageProxy.planes[0].buffer
            val data = ByteArray(buffer.capacity())
            buffer.get(data)

            val width = imageProxy.width
            val height = imageProxy.height
            val mat = Mat(height + height / 2, width, CvType.CV_8UC1)
            mat.put(0, 0, data)

            val grayMat = Mat()
            Imgproc.cvtColor(mat, grayMat, Imgproc.COLOR_YUV2GRAY_420)

            if (prevGray == null) {
                prevGray = grayMat.clone()
                imageProxy.close()
                return
            }

            val flow = Mat()
            Video.calcOpticalFlowFarneback(prevGray, grayMat, flow, 0.5, 3, 15, 3, 5, 1.2, 0)

            val flowImage = drawOpticalFlow(flow)

            runOnUiThread {
                val bitmap = Bitmap.createBitmap(flowImage.width(), flowImage.height(), Bitmap.Config.ARGB_8888)
                val canvas = Canvas(bitmap)
                val paint = Paint().apply {
                    color = Color.RED
                    strokeWidth = 2f
                }

                val matBitmap = Bitmap.createBitmap(flowImage.width(), flowImage.height(), Bitmap.Config.ARGB_8888)
                org.opencv.android.Utils.matToBitmap(flowImage, matBitmap)

                canvas.drawBitmap(matBitmap, 0f, 0f, paint)
                previewView.overlay.clear()
                previewView.overlay.add(BitmapDrawable(resources, bitmap))
            }

            prevGray?.release()
            prevGray = grayMat.clone()

            mat.release()
            flow.release()
            grayMat.release()

        } finally {
            imageProxy.close()
        }
    }

    private fun drawOpticalFlow(flow: Mat): Mat {
        val flowImage = Mat.zeros(flow.size(), CvType.CV_8UC3)

        for (y in 0 until flow.rows()) {
            for (x in 0 until flow.cols()) {
                val flowAtPoint = flow.get(y, x)
                val flowX = flowAtPoint[0]
                val flowY = flowAtPoint[1]

                val startPoint = Point(x.toDouble(), y.toDouble())
                val endPoint = Point(x + flowX, y + flowY)

                Imgproc.line(flowImage, startPoint, endPoint, Scalar(0.0, 255.0, 0.0))
                Imgproc.circle(flowImage, endPoint, 1, Scalar(0.0, 255.0, 0.0), -1)
            }
        }
        return flowImage
    }

    companion object {
        private const val REQUEST_CODE_CAMERA_PERMISSION = 101
        private val PERMISSIONS = arrayOf(Manifest.permission.CAMERA)
    }
}
