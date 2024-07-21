// Copyright (c) 2020 Facebook, Inc. and its affiliates.
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.
package org.pytorch.demo.objectdetection

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.SystemClock
import android.util.Size
import android.view.TextureView
import android.widget.Toast
import androidx.annotation.UiThread
import androidx.annotation.WorkerThread
import androidx.camera.core.CameraX
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageAnalysisConfig
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
import androidx.camera.core.Preview.OnPreviewOutputUpdateListener
import androidx.camera.core.Preview.PreviewOutput
import androidx.camera.core.PreviewConfig
import androidx.core.app.ActivityCompat

abstract class AbstractCameraXActivity<R> : BaseModuleActivity() {
    private var mLastAnalysisResultTime: Long = 0

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
        } else {
            setupCameraX()
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
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
        val textureView = cameraPreviewTextureView

        val previewConfig =
            PreviewConfig.Builder()
                .setTargetResolution(Size(960, 1280))
                .setTargetRotation(windowManager.defaultDisplay.rotation) //.setTargetAspectRatio(new Rational(1,1))
                .build()
        val preview = Preview(previewConfig)
        //preview.setOnPreviewOutputUpdateListener(output ->
        //textureView.setSurfaceTexture(output.getSurfaceTexture()));
        preview.onPreviewOutputUpdateListener = getSurfaceListener(textureView)

        val imageAnalysisConfig =
            mBackgroundHandler?.let {
                ImageAnalysisConfig.Builder()
                    .setTargetResolution(
                        Size(
                            960,
                            1280
                        )
                    ) //.setTargetRotation(getWindowManager().getDefaultDisplay().getRotation())
                    //.setTargetAspectRatio(new Rational(1,1))
                    .setCallbackHandler(it)
                    .setImageReaderMode(ImageAnalysis.ImageReaderMode.ACQUIRE_LATEST_IMAGE)
                    .build()
            }
        val imageAnalysis = ImageAnalysis(imageAnalysisConfig)
        imageAnalysis.analyzer =
            ImageAnalysis.Analyzer { image: ImageProxy?, rotationDegrees: Int ->
                //Inference time
                //if (SystemClock.elapsedRealtime() - mLastAnalysisResultTime < 500) {
                //    return;
                //}
                val result = analyzeImage(image, rotationDegrees)
                if (result != null) {

                    val mElapsedTime = SystemClock.elapsedRealtime() - mLastAnalysisResultTime
                    mLastAnalysisResultTime = SystemClock.elapsedRealtime()
                    runOnUiThread { applyToUiAnalyzeImageResult(result,mElapsedTime) }
                }
            }

        CameraX.bindToLifecycle(this, preview, imageAnalysis)
    }


    private fun getSurfaceListener(textureView: TextureView): OnPreviewOutputUpdateListener {
        return OnPreviewOutputUpdateListener { output: PreviewOutput ->
            val newTexture = output.surfaceTexture
            textureView.setSurfaceTexture(newTexture)
        }
    }

    @WorkerThread
    protected abstract fun analyzeImage(image: ImageProxy?, rotationDegrees: Int): R?

    @UiThread
    protected abstract fun applyToUiAnalyzeImageResult(result: R, mElapsedTime: Long)

    companion object {
        private const val REQUEST_CODE_CAMERA_PERMISSION = 200
        private val PERMISSIONS = arrayOf(Manifest.permission.CAMERA)
    }
}
