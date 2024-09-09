// Copyright (c) 2020 Facebook, Inc. and its affiliates.
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.
package org.pytorch.demo.objectdetection

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.SurfaceTexture
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.util.Size
import android.view.Surface
import android.view.TextureView
import android.widget.Toast
import androidx.annotation.UiThread
import androidx.annotation.WorkerThread
import androidx.camera.core.AspectRatio
import androidx.camera.core.CameraSelector

import androidx.camera.core.CameraX
import androidx.camera.core.ImageAnalysis
//import androidx.camera.core.ImageAnalysisConfig
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
//import androidx.camera.core.Preview.OnPreviewOutputUpdateListener
//import androidx.camera.core.Preview.PreviewOutput
import androidx.camera.core.SurfaceRequest
import androidx.camera.core.resolutionselector.AspectRatioStrategy
//import androidx.camera.core.PreviewConfig
import androidx.camera.core.resolutionselector.ResolutionSelector
import androidx.camera.core.resolutionselector.ResolutionStrategy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors



abstract class AbstractCameraXActivity<R> : BaseModuleActivity() {

    private var mLastAnalysisResultTime: Long = 0
    private lateinit var cameraExecutor: ExecutorService
    private lateinit var textureView : TextureView

    protected abstract var mResultQueue : ResultsQueueSet
    protected abstract val contentViewLayoutId: Int
    protected abstract val cameraPreviewTextureView: TextureView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        //setContentView(contentViewLayoutId)

        startBackgroundThread()

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                PERMISSIONS,
                REQUEST_CODE_CAMERA_PERMISSION
            )
        }
        textureView = cameraPreviewTextureView
        textureView.surfaceTextureListener = object : TextureView.SurfaceTextureListener{
            override fun onSurfaceTextureAvailable(
                surface: SurfaceTexture,
                width: Int,
                height: Int
            ) {
                setupCameraX()
            }

            override fun onSurfaceTextureSizeChanged(
                surface: SurfaceTexture,
                width: Int,
                height: Int
            ) {
            }

            override fun onSurfaceTextureDestroyed(surface: SurfaceTexture): Boolean {
                return true
            }

            override fun onSurfaceTextureUpdated(surface: SurfaceTexture) {
                //textureView.setSurfaceTexture(surface)
            }

        }

        cameraExecutor = Executors.newSingleThreadExecutor()


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
                    "You can't use object detection example without granting CAMERA permission",
                    Toast.LENGTH_LONG
                )
                    .show()
                finish()
            } else {
                setupCameraX()
            }
        }
    }

    private fun setupCameraX() {

        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener({
            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()
            val targetResolutionSize = Size(360,480)

            val mResolutionSelector = ResolutionSelector.Builder()
//                .setAspectRatioStrategy(
//                    AspectRatioStrategy(
//
//                        AspectRatio.RATIO_4_3,
//                        AspectRatioStrategy.FALLBACK_RULE_NONE
//                    )
//                )
                .setResolutionStrategy(ResolutionStrategy(targetResolutionSize,ResolutionStrategy.FALLBACK_RULE_CLOSEST_HIGHER_THEN_LOWER))
                .build()
            Log.i("Textureview Rotation",textureView.display.rotation.toString())
            val preview = Preview.Builder()
                //.setTargetRotation(textureView.display.rotation)
                .setResolutionSelector(mResolutionSelector)
                .setTargetRotation(this.display!!.rotation)
                .build()
            preview.setSurfaceProvider {
                val surface = Surface(textureView.surfaceTexture)
                it.provideSurface(surface, cameraExecutor) { result ->
                    when (result.resultCode) {
                        SurfaceRequest.Result.RESULT_SURFACE_USED_SUCCESSFULLY -> {
                            Log.d("CameraXApp", "Surface was used successfully.")
                        }

                        SurfaceRequest.Result.RESULT_INVALID_SURFACE -> {
                            Log.e("CameraXApp", "Invalid surface.")
                        }

                        SurfaceRequest.Result.RESULT_SURFACE_ALREADY_PROVIDED -> {
                            Log.e("CameraXApp", "Surface already provided.")
                        }

                        SurfaceRequest.Result.RESULT_REQUEST_CANCELLED -> {
                            Log.e("CameraXApp", "Surface request cancelled.")
                        }

                        SurfaceRequest.Result.RESULT_WILL_NOT_PROVIDE_SURFACE -> {
                            Log.e("CameraXApp", "Will not provide surface")
                        }
                    }
                }
            }
            val imageAnalysis = ImageAnalysis.Builder()
                //.setTargetAspectRatio(AspectRatio.RATIO_4_3)
                .setResolutionSelector(mResolutionSelector)
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .build()
            imageAnalysis.setAnalyzer(cameraExecutor, ObjectDetectAnalyzer())
            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageAnalysis)
            } catch (e: Exception) {
                Log.e("CameraXApp", "Camera Failed", e)
            }
        }, ContextCompat.getMainExecutor(this))
    }
        
        //Code for older camera version
//        val previewConfig =
//            PreviewConfig.Builder()
//                .setTargetResolution(Size(1080, 1440))
//                .setTargetRotation(windowManager.defaultDisplay.rotation) //.setTargetAspectRatio(new Rational(1,1))
//                .build()
//        val preview = Preview(previewConfig)


        //preview.setOnPreviewOutputUpdateListener(output ->
        //textureView.setSurfaceTexture(output.getSurfaceTexture()));

        //preview.onPreviewOutputUpdateListener = getSurfaceListener(textureView)

//        val imageAnalysisConfig =
//            mBackgroundHandler?.let {
//                ImageAnalysisConfig.Builder()
//                    .setTargetResolution(
//                        Size(
//                            1080,
//                            1440
//                        )
//                    ) //.setTargetRotation(getWindowManager().getDefaultDisplay().getRotation())
//                    //.setTargetAspectRatio(new Rational(1,1))
//                    .setCallbackHandler(it)
//                    .setImageReaderMode(ImageAnalysis.ImageReaderMode.ACQUIRE_LATEST_IMAGE)
//                    .build()
//            }
//        val imageAnalysis = ImageAnalysis(imageAnalysisConfig)
        
//        imageAnalysis.analyzer =
//            ImageAnalysis.Analyzer { image: ImageProxy?, rotationDegrees: Int ->
//                //Inference time
//                //if (SystemClock.elapsedRealtime() - mLastAnalysisResultTime < 500) {
//                //    return;
//                //}
//                val result = analyzeImage(image, rotationDegrees)
//                if (result != null) {
//
//                    val mElapsedTime = SystemClock.elapsedRealtime() - mLastAnalysisResultTime
//                    mLastAnalysisResultTime = SystemClock.elapsedRealtime()
//                    runOnUiThread { applyToUiAnalyzeImageResult(result,mElapsedTime) }
//                }
//            }

        //CameraX.bindToLifecycle(this, preview, imageAnalysis)
//    }


//    private fun getSurfaceListener(textureView: TextureView): OnPreviewOutputUpdateListener {
//        return OnPreviewOutputUpdateListener { output: PreviewOutput ->
//            val newTexture = output.surfaceTexture
//            textureView.setSurfaceTexture(newTexture)
//        }
//    }


    private inner class ObjectDetectAnalyzer() : ImageAnalysis.Analyzer {
        override fun analyze(image: ImageProxy) {
            val result = analyzeImage(image)
                if (result != null) {
                    val mElapsedTime = SystemClock.elapsedRealtime() - mLastAnalysisResultTime
                    mLastAnalysisResultTime = SystemClock.elapsedRealtime()
                    runOnUiThread { applyToUiAnalyzeImageResult(result,mElapsedTime) }
                }
            image.close()
        }

    }

    @Override
    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
    }

    @WorkerThread
    protected abstract fun analyzeImage(image: ImageProxy?): R?

    @UiThread
    protected abstract fun applyToUiAnalyzeImageResult(result: R, mElapsedTime: Long)

    companion object {
        private const val REQUEST_CODE_CAMERA_PERMISSION = 200
        private val PERMISSIONS = arrayOf(Manifest.permission.CAMERA)
    }
}
