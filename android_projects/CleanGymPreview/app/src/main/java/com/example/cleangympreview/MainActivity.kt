package com.example.cleangympreview

//Camera Imports
import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Paint
import android.graphics.SurfaceTexture
import android.hardware.camera2.CameraCaptureSession
import android.hardware.camera2.CameraDevice
import android.hardware.camera2.CameraManager
import androidx.camera.core.Preview
import android.hardware.camera2.params.SessionConfiguration
import android.os.Bundle
import android.os.Handler
import android.os.HandlerThread
import android.os.SystemClock
import android.view.Surface
import android.view.TextureView
import android.widget.Button
import androidx.activity.ComponentActivity
import androidx.camera.core.impl.PreviewConfig
import androidx.camera.core.impl.SessionConfig
import android.graphics.Canvas

import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class MainActivity : ComponentActivity() {
    //private lateinit var model:
    private lateinit var textureView: TextureView
    //private lateinit var startButton: Button
    private lateinit var bitmap: Bitmap
    private lateinit var boxPaint: Paint
    private lateinit var textPaint: Paint

    private lateinit var cameraManager: CameraManager
    private lateinit var cameraDevice: CameraDevice
    private lateinit var cameraExecutor: ExecutorService
    private lateinit var handler : Handler
    private lateinit var yolov5TFLiteDetector: Yolo5lite
    private var lastTime: Long = 0L

    private val THRESHOLD = 0.4f

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        getPermission()

        val handlerThread = HandlerThread("VideoThread")
        handlerThread.start()
        handler = Handler(handlerThread.looper)

        cameraManager = getSystemService(Context.CAMERA_SERVICE) as CameraManager
        textureView = findViewById(R.id.textureView)
        textureView.surfaceTextureListener = object : TextureView.SurfaceTextureListener{
            override fun onSurfaceTextureAvailable(
                surface: SurfaceTexture,
                width: Int,
                height: Int
            ) {
                openCamera()
            }

            override fun onSurfaceTextureSizeChanged(
                surface: SurfaceTexture,
                width: Int,
                height: Int
            ) {

            }

            override fun onSurfaceTextureDestroyed(surface: SurfaceTexture): Boolean {
                return false
            }

            override fun onSurfaceTextureUpdated(surface: SurfaceTexture) {
                //if laggy, try do detection after a period of time
                val currTime = SystemClock.elapsedRealtime()
                if (currTime-lastTime >=800){
                    lastTime = currTime
                    //run detection things
                    runYolo(textureView.bitmap!!)

                }
            }


        }

        cameraExecutor = Executors.newSingleThreadExecutor()
        //startButton = findViewById(R.id.start_processing_button)


        yolov5TFLiteDetector = Yolo5lite()
        yolov5TFLiteDetector.setModelFile("best-fp16.tflite")
        yolov5TFLiteDetector.initModel(this)

        boxPaint = Paint()
        boxPaint.strokeWidth = 5F
        boxPaint.style = Paint.Style.STROKE
        boxPaint.setColor(Color.RED)

        textPaint = Paint()
        textPaint.textSize = 50F
        textPaint.setColor(Color.GREEN)
        textPaint.style = Paint.Style.FILL

    }

    private fun runYolo(bitmap: Bitmap) {
        val recognitions = yolov5TFLiteDetector.detect(bitmap)
        var mutableBitmap = bitmap.copy(Bitmap.Config.ARGB_8888, true)
        val canvas = Canvas(mutableBitmap)

        for (recoganization : Recognition in recognitions){
            if(recoganization.confidence>THRESHOLD){
                var location = recoganization.getLocation()
                canvas.drawRect(location,boxPaint)
                canvas.drawText(recoganization.labelName+":"+recoganization.confidence,
                    location.left,location.top,textPaint)
            }
        }
        textureView.unlockCanvasAndPost(canvas)


    }

    @SuppressLint("MissingPermission")
    private fun openCamera() {
        //using selfie cam
        cameraManager.openCamera(cameraManager.cameraIdList[0],object : CameraDevice.StateCallback(){
            override fun onOpened(camera: CameraDevice) {
                cameraDevice = camera
                val surfaceTexture  = textureView.surfaceTexture
                val surface = Surface(surfaceTexture)
                val captureRequest = cameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW)
                captureRequest.addTarget(surface)

                cameraDevice.createCaptureSession(listOf(surface), object: CameraCaptureSession.StateCallback(){
                    override fun onConfigured(p0: CameraCaptureSession) {
                        p0.setRepeatingRequest(captureRequest.build(), null, null)
                    }
                    override fun onConfigureFailed(p0: CameraCaptureSession) {
                    }
                },handler)
            }

            override fun onDisconnected(camera: CameraDevice) {
            }

            override fun onError(camera: CameraDevice, error: Int) {
            }
        },handler)


    }



    override fun onDestroy() {
        super.onDestroy()

        //model.close()
    }

    private fun getPermission() {
        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CAMERA
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 101)
        }
    }

}

