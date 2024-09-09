package org.pytorch.demo.objectdetection

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle

import android.util.Log
import android.util.Size
import android.widget.TextView

import android.widget.Toast
import androidx.annotation.OptIn
import androidx.annotation.WorkerThread
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ExperimentalGetImage
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.core.resolutionselector.ResolutionSelector
import androidx.camera.core.resolutionselector.ResolutionStrategy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.common.InputImage

import com.google.mlkit.vision.pose.PoseDetection
import com.google.mlkit.vision.pose.PoseDetector
import com.google.mlkit.vision.pose.PoseLandmark
import com.google.mlkit.vision.pose.defaults.PoseDetectorOptions
import kotlin.math.atan2


class PoseEstimationActivity: AppCompatActivity() {
    private lateinit var previewView: PreviewView
    private lateinit var poseView : PoseDetectionView
    private lateinit var poseDetector: PoseDetector
    private lateinit var poseText : TextView

    private var landMarksList : MutableList<PoseLandmark>? = null
//    private lateinit var leftShoulder : PoseLandmark
//    private lateinit var rightShoulder : PoseLandmark
//    private lateinit var leftElbow : PoseLandmark
//    private lateinit var rightElbow : PoseLandmark
//    private lateinit var leftWrist : PoseLandmark
//    private lateinit var rightWrist : PoseLandmark
//    private lateinit var leftHip : PoseLandmark
//    private lateinit var rightHip : PoseLandmark
//    private lateinit var leftKnee : PoseLandmark
//    private lateinit var rightKnee : PoseLandmark
//    private lateinit var leftAnkle : PoseLandmark
//    private lateinit var rightAnkle : PoseLandmark

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_pose_estimation)
        previewView = findViewById(R.id.posePreview)
        poseView = findViewById(R.id.poseOverlay)
        poseText = findViewById(R.id.poseText)

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
        val options = PoseDetectorOptions.Builder()
            .setDetectorMode(PoseDetectorOptions.STREAM_MODE)
            .build()
        poseDetector = PoseDetection.getClient(options)
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
            val targetResolutionSize = Size(1440,1440)
            val mResolutionSelector = ResolutionSelector.Builder()
//                .setAspectRatioStrategy(
//                    AspectRatioStrategy(
//
//                        AspectRatio.RATIO_4_3,
//                        AspectRatioStrategy.FALLBACK_RULE_NONE
//                    )
//                )
                .setResolutionStrategy(
                    ResolutionStrategy(targetResolutionSize,
                        ResolutionStrategy.FALLBACK_RULE_CLOSEST_HIGHER_THEN_LOWER)
                )
                .build()
            val preview = androidx.camera.core.Preview.Builder()
                .setResolutionSelector(mResolutionSelector).build().also {
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

    @OptIn(ExperimentalGetImage::class)
    @WorkerThread
    private fun processImage(imageProxy: ImageProxy) {
        Log.i("Pose Debug","Processing pose")
        val mediaImage = imageProxy.image
        if (mediaImage != null) {
            val image = InputImage.fromMediaImage(mediaImage, imageProxy.imageInfo.rotationDegrees)
            var result = poseDetector.process(image)
            // Get all PoseLandmarks. If no person was detected, the list will be empty
            result.addOnSuccessListener {
                pose ->
                landMarksList = pose.allPoseLandmarks
                Log.i("Pose result",result.toString())
                runOnUiThread{
                    poseView.setLankMarks(landMarksList)
                    poseView.invalidate()

                    poseText.setText("Landmark size: "+landMarksList!!.size.toString())
                }
                // Or get specific PoseLandmarks individually. These will all be null if no person
                // was detected
//                leftShoulder = pose.getPoseLandmark(PoseLandmark.LEFT_SHOULDER)
//                rightShoulder = pose.getPoseLandmark(PoseLandmark.RIGHT_SHOULDER)
//                leftElbow = pose.getPoseLandmark(PoseLandmark.LEFT_ELBOW)
//                rightElbow = pose.getPoseLandmark(PoseLandmark.RIGHT_ELBOW)
//                leftWrist = pose.getPoseLandmark(PoseLandmark.LEFT_WRIST)
//                rightWrist = pose.getPoseLandmark(PoseLandmark.RIGHT_WRIST)
//                leftHip = pose.getPoseLandmark(PoseLandmark.LEFT_HIP)
//                rightHip = pose.getPoseLandmark(PoseLandmark.RIGHT_HIP)
//                leftKnee = pose.getPoseLandmark(PoseLandmark.LEFT_KNEE)
//                rightKnee = pose.getPoseLandmark(PoseLandmark.RIGHT_KNEE)
//                leftAnkle = pose.getPoseLandmark(PoseLandmark.LEFT_ANKLE)
//                rightAnkle = pose.getPoseLandmark(PoseLandmark.RIGHT_ANKLE)
                //leftPinky = pose.getPoseLandmark(PoseLandmark.LEFT_PINKY)
                //rightPinky = pose.getPoseLandmark(PoseLandmark.RIGHT_PINKY)
                //leftIndex = pose.getPoseLandmark(PoseLandmark.LEFT_INDEX)
                //rightIndex = pose.getPoseLandmark(PoseLandmark.RIGHT_INDEX)
                //leftThumb = pose.getPoseLandmark(PoseLandmark.LEFT_THUMB)
                //rightThumb = pose.getPoseLandmark(PoseLandmark.RIGHT_THUMB)
//                val leftHeel = pose.getPoseLandmark(PoseLandmark.LEFT_HEEL)
//                val rightHeel = pose.getPoseLandmark(PoseLandmark.RIGHT_HEEL)
//                val leftFootIndex = pose.getPoseLandmark(PoseLandmark.LEFT_FOOT_INDEX)
//                val rightFootIndex = pose.getPoseLandmark(PoseLandmark.RIGHT_FOOT_INDEX)
//                val nose = pose.getPoseLandmark(PoseLandmark.NOSE)
//                val leftEyeInner = pose.getPoseLandmark(PoseLandmark.LEFT_EYE_INNER)
//                val leftEye = pose.getPoseLandmark(PoseLandmark.LEFT_EYE)
//                val leftEyeOuter = pose.getPoseLandmark(PoseLandmark.LEFT_EYE_OUTER)
//                val rightEyeInner = pose.getPoseLandmark(PoseLandmark.RIGHT_EYE_INNER)
//                val rightEye = pose.getPoseLandmark(PoseLandmark.RIGHT_EYE)
//                val rightEyeOuter = pose.getPoseLandmark(PoseLandmark.RIGHT_EYE_OUTER)
//                val leftEar = pose.getPoseLandmark(PoseLandmark.LEFT_EAR)
//                val rightEar = pose.getPoseLandmark(PoseLandmark.RIGHT_EAR)
//                val leftMouth = pose.getPoseLandmark(PoseLandmark.LEFT_MOUTH)
//                val rightMouth = pose.getPoseLandmark(PoseLandmark.RIGHT_MOUTH)


            }
            result.addOnFailureListener { e -> Log.e("Pose",e.stackTraceToString()) }


            
            //imageProxy.close()
        }
    }

    fun getAngle(firstPoint: PoseLandmark, midPoint: PoseLandmark, lastPoint: PoseLandmark): Double {
        var result = Math.toDegrees(
            (atan2(lastPoint.getPosition().y - midPoint.getPosition().y,
                lastPoint.getPosition().x - midPoint.getPosition().x)
                    - atan2(firstPoint.getPosition().y - midPoint.getPosition().y,
                firstPoint.getPosition().x - midPoint.getPosition().x)).toDouble()
        )
        result = Math.abs(result) // Angle should never be negative
        if (result > 180) {
            result = 360.0 - result // Always get the acute representation of the angle
        }
        return result
    }

    companion object {
        private const val REQUEST_CODE_CAMERA_PERMISSION = 101
        private val PERMISSIONS = arrayOf(Manifest.permission.CAMERA)
    }
}
