package com.example.objectdetectionpreview

import android.Manifest
import android.annotation.SuppressLint
import android.content.ContentValues
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.SurfaceTexture
import android.hardware.camera2.CameraCaptureSession
import android.hardware.camera2.CameraDevice
import android.hardware.camera2.CameraManager
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.HandlerThread
import android.provider.MediaStore
import android.service.controls.templates.StatelessTemplate
import android.util.Log
import android.view.Surface
import android.view.TextureView
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.video.MediaStoreOutputOptions
import androidx.camera.video.Quality
import androidx.camera.video.QualitySelector
import androidx.camera.video.Recorder
import androidx.camera.video.Recording
import androidx.camera.video.VideoCapture
import androidx.camera.video.VideoRecordEvent
import androidx.camera.view.PreviewView
import androidx.compose.foundation.Image
import androidx.core.content.ContextCompat
import androidx.core.content.PermissionChecker
import androidx.lifecycle.ReportFragment.Companion.reportFragment
import com.example.objectdetectionpreview.databinding.ActivityMainBinding
import com.example.objectdetectionpreview.ml.BestFp16
import org.pytorch.LiteModuleLoader
import org.pytorch.Module
import org.tensorflow.lite.DataType
import org.tensorflow.lite.support.image.TensorImage
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer
import org.tensorflow.lite.support.image.ops.ResizeOp
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Locale
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors


typealias LumaListener = (luma: Double) -> Unit

class MainActivity : AppCompatActivity() {
    private lateinit var viewBinding: ActivityMainBinding
    private lateinit var previewView: PreviewView
    private lateinit var textureView: TextureView
    private lateinit var imageView: ImageView
    private lateinit var textView: TextView
    private lateinit var bitmap: Bitmap
    private lateinit var mModule : Module
    private lateinit var imageProcessor: org.tensorflow.lite.support.image.ImageProcessor

    private var videoCapture: VideoCapture<Recorder>? = null
    private var recording: Recording? = null
    //private val paint = Paint()

    private lateinit var handler:Handler
    private lateinit var cameraExecutor: ExecutorService
    private lateinit var cameraManager: CameraManager
    private lateinit var cameraDevice: CameraDevice
    private lateinit var tfModel:BestFp16

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Request camera permissions
        if (allPermissionsGranted()) {
            //startCamera()
        } else {
            requestPermissions()
        }

        val classes = loadClasses("classes.txt")
        println("loaded classes")
        //mModule = LiteModuleLoader.load(assetFilePath(this.applicationContext,"best.torchscript.ptl"))
        val tfModel = BestFp16.newInstance(this)
        println("loaded module")

        imageProcessor = org.tensorflow.lite.support.image.ImageProcessor.Builder()
            .add(ResizeOp(640,640,ResizeOp.ResizeMethod.BILINEAR)).build()

        val handlerThread = HandlerThread("videoThread")
        handlerThread.start()
        handler = Handler(handlerThread.looper)

        viewBinding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(viewBinding.root)
        previewView = findViewById(R.id.viewFinder)
        textureView = findViewById(R.id.textureView)
        imageView = findViewById(R.id.imageView)
        textView = findViewById(R.id.textView)

        cameraManager = getSystemService(Context.CAMERA_SERVICE) as CameraManager

        textureView.surfaceTextureListener = object:TextureView.SurfaceTextureListener{
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
                TODO("Not yet implemented")
            }

            override fun onSurfaceTextureDestroyed(surface: SurfaceTexture): Boolean {
                TODO("Not yet implemented")
            }

            override fun onSurfaceTextureUpdated(surface: SurfaceTexture) {
                bitmap = textureView.bitmap!!

                var image = TensorImage(DataType.FLOAT32)
                image.load(bitmap)
                image = imageProcessor.process(image)
                val tensorBuffer = TensorBuffer.createFixedSize(intArrayOf(1, 640, 640, 3), DataType.FLOAT32)
                tensorBuffer.loadBuffer(image.buffer)
                val timeStart = System.currentTimeMillis()
                val outputs = tfModel.process(tensorBuffer)
                val timeEnd = System.currentTimeMillis()
                println(timeEnd-timeStart)
                //println("Shape of the tensor: (${outputs.outputFeature0AsTensorBuffer.shape.joinToString(", ")})")
                val outputShape = intArrayOf(1,25200,10)
                val outputArray = Array(outputShape[0]) {
                    Array(outputShape[1]) {
                        FloatArray(outputShape[2])
                    }
                }

                val floatBuffer = outputs.outputFeature0AsTensorBuffer.floatArray
                var index = 0
                for (i in 0 until outputShape[0]) {
                    for (j in 0 until outputShape[1]) {
                        for (k in 0 until outputShape[2]) {
                            outputArray[i][j][k] = floatBuffer[index++]
                        }
                    }
                }



  //              var mutable = bitmap.copy(Bitmap.Config.ARGB_8888,true)
    //            val canvas = android.graphics.Canvas(mutable)

      //          val h = mutable.height
        //        val w = mutable.width

                //paint.textSize = h/15f
                //paint.strokeWidth = h/85f
                //var x=  0

                //scores.forEachIndex()


            }

        }
        // Set up the listeners for take photo and video capture buttons
        //viewBinding.videoCaptureButton.setOnClickListener { captureVideo() }

        cameraExecutor = Executors.newSingleThreadExecutor()
    }



    private fun loadClasses(classFilePath: String): List<String> {
        var result = mutableListOf<String>()
        application.assets.open(classFilePath).bufferedReader().useLines {
            lines ->lines.forEach {
                result.add(it)
            }
        }

        //result.forEach{println(it)}
        return result
    }

    @Throws(IOException::class)
    fun assetFilePath(context: Context, assetName: String?): String {
        println(context.filesDir)
        val file = File(context.filesDir, assetName)
        if (file.exists() && file.length() > 0) {
            return file.absolutePath
        }

        context.assets.open(assetName!!).use { `is` ->
            FileOutputStream(file).use { os ->
                val buffer = ByteArray(4 * 1024)
                var read: Int
                while ((`is`.read(buffer).also { read = it }) != -1) {
                    os.write(buffer, 0, read)
                }
                os.flush()
            }
            return file.absolutePath
        }
    }

    @SuppressLint("MissingPermission")
    private fun openCamera() {

        cameraManager.openCamera(cameraManager.cameraIdList[1],object:CameraDevice.StateCallback(){
            override fun onOpened(p0: CameraDevice) {
                cameraDevice = p0
                var surfaceTexture  = textureView.surfaceTexture
                var surface = Surface(surfaceTexture)
                var captureRequest = cameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW)
                captureRequest.addTarget(surface)
                cameraDevice.createCaptureSession(listOf(surface),object:CameraCaptureSession.StateCallback(){
                    override fun onConfigured(session: CameraCaptureSession) {
                        session.setRepeatingRequest(captureRequest.build(),null,null)
                    }

                    override fun onConfigureFailed(session: CameraCaptureSession) {
                        TODO("Not yet implemented")
                    }
                },handler)

            }

            override fun onDisconnected(camera: CameraDevice) {
                TODO("Not yet implemented")
            }

            override fun onError(camera: CameraDevice, error: Int) {
                TODO("Not yet implemented")
            }
        },handler)

    }

    //This
    // Implements VideoCapture use case, including start and stop capturing.
    private fun captureVideo() {
        val videoCapture = this.videoCapture ?: return

        viewBinding.videoCaptureButton.isEnabled = false

        val curRecording = recording
        if (curRecording != null) {
            // Stop the current recording session.
            curRecording.stop()
            recording = null
            return
        }

        // create and start a new recording session
        val name = SimpleDateFormat(FILENAME_FORMAT, Locale.US)
            .format(System.currentTimeMillis())
        val contentValues = ContentValues().apply {
            put(MediaStore.MediaColumns.DISPLAY_NAME, name)
            put(MediaStore.MediaColumns.MIME_TYPE, "video/mp4")
            if (Build.VERSION.SDK_INT > Build.VERSION_CODES.P) {
                put(MediaStore.Video.Media.RELATIVE_PATH, "Movies/CameraX-Video")
            }
        }

        val mediaStoreOutputOptions = MediaStoreOutputOptions
            .Builder(contentResolver, MediaStore.Video.Media.EXTERNAL_CONTENT_URI)
            .setContentValues(contentValues)
            .build()
        recording = videoCapture.output
            .prepareRecording(this, mediaStoreOutputOptions)
            .apply {
                if (PermissionChecker.checkSelfPermission(this@MainActivity,
                        Manifest.permission.RECORD_AUDIO) ==
                    PermissionChecker.PERMISSION_GRANTED)
                {
                    withAudioEnabled()
                }
            }
            .start(ContextCompat.getMainExecutor(this)) { recordEvent ->
                when(recordEvent) {
                    is VideoRecordEvent.Start -> {
                        viewBinding.videoCaptureButton.apply {
                            text = getString(R.string.stop_capture)
                            isEnabled = true
                        }
                    }
                    is VideoRecordEvent.Finalize -> {
                        if (!recordEvent.hasError()) {
                            val msg = "Video capture succeeded: " +
                                    "${recordEvent.outputResults.outputUri}"
                            Toast.makeText(baseContext, msg, Toast.LENGTH_SHORT)
                                .show()
                            Log.d(TAG, msg)
                        } else {
                            recording?.close()
                            recording = null
                            Log.e(TAG, "Video capture ends with error: " +
                                    "${recordEvent.error}")
                        }
                        viewBinding.videoCaptureButton.apply {
                            text = getString(R.string.start_capture)
                            isEnabled = true
                        }
                    }
                }
            }
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener({
            // Used to bind the lifecycle of cameras to the lifecycle owner
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

            // Preview
            val preview = Preview.Builder()
                .build()
                .also {
                    it.setSurfaceProvider(viewBinding.viewFinder.surfaceProvider)

                }

//            val processedView = Preview.Builder().build()
//            processedView.setSurfaceProvider { request ->
//                val surfaceTexture = textureView.surfaceTexture
//                if (surfaceTexture != null) {
//                    surfaceTexture.setDefaultBufferSize(
//                        request.resolution.width, request.resolution.height
//                    )
//                    val surface = Surface(surfaceTexture)
//                    request.provideSurface(
//                        surface,
//                        ContextCompat.getMainExecutor(this@MainActivity)
//                    ) { result ->
                        // Handle surface events
//                        when (result.resultCode) {
//                            SurfaceRequest.Result.RESULT_SURFACE_USED_SUCCESSFULLY -> {
//                                Log.d("CameraXApp", "Surface used successfully")
//                            }
//
//                            SurfaceRequest.Result.RESULT_SURFACE_ALREADY_PROVIDED -> {
//                                Log.d("CameraXApp", "Surface already provided")
//                            }
//                        }
//                    }
//                }
//            }
            // Video
            val recorder = Recorder.Builder()
                .setQualitySelector(QualitySelector.from(Quality.HIGHEST))
                .build()
            videoCapture = VideoCapture.withOutput(recorder)

            // Select back camera as a default
            val cameraSelector = CameraSelector.DEFAULT_FRONT_CAMERA

            try {
                // Unbind use cases before rebinding
                cameraProvider.unbindAll()

                // Bind use cases to camera
                cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview,videoCapture)

            } catch(exc: Exception) {
                Log.e(TAG, "Use case binding failed", exc)
            }

        }, ContextCompat.getMainExecutor(this))
    }

    private val activityResultLauncher =
        registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) {
            permission ->
            var permissionGranted = true
            permission.entries.forEach{
                if (it.key in REQUIRED_PERMISSIONS && it.value==false)
                    permissionGranted = false
            }
            if (!permissionGranted){
                Toast.makeText(
                    baseContext,
                    "Permission Request Denied",
                    Toast.LENGTH_SHORT
                ).show()
            } else {
                //startCamera()
            }
        }
    private fun requestPermissions() {
        activityResultLauncher.launch(REQUIRED_PERMISSIONS)
    }

    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
        ContextCompat.checkSelfPermission(
            baseContext, it) == PackageManager.PERMISSION_GRANTED
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
        tfModel.close()
    }

    companion object {
        private const val TAG = "CameraXApp"
        private const val FILENAME_FORMAT = "yyyy-MM-dd-HH-mm-ss-SSS"
        private val REQUIRED_PERMISSIONS =
            mutableListOf (
                Manifest.permission.CAMERA,
                Manifest.permission.RECORD_AUDIO
            ).apply {
                if (Build.VERSION.SDK_INT <= Build.VERSION_CODES.P) {
                    add(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                }
            }.toTypedArray()
    }

}

