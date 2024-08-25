package org.pytorch.demo.objectdetection

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageFormat
import android.graphics.Matrix
import android.graphics.Rect
import android.graphics.YuvImage
import android.media.Image
import android.os.Bundle
import android.util.Log
import android.view.TextureView
import android.view.View
import android.view.ViewStub
import android.widget.Button
import android.widget.TextView
import androidx.annotation.OptIn
import androidx.annotation.WorkerThread
import androidx.camera.core.ExperimentalGetImage
import androidx.camera.core.ImageProxy
import org.pytorch.IValue
import org.pytorch.LiteModuleLoader
import org.pytorch.Module
import org.pytorch.Tensor
import org.pytorch.demo.objectdetection.ObjectDetectionActivity.AnalysisResult
import org.pytorch.demo.objectdetection.PrePostProcessor.outputsToNMSPredictions
import org.pytorch.torchvision.TensorImageUtils
import java.io.ByteArrayOutputStream
import java.io.IOException

class ObjectDetectionActivity: AbstractCameraXActivity<AnalysisResult?>() {
    private var mModule: Module? = null
    private var mResultView: ResultView? = null
    private var mResultTextView:TextView? = null
    override lateinit var cameraPreviewTextureView: TextureView
    override val contentViewLayoutId: Int = R.layout.activity_object_detection
    override var mResultQueue = ResultsQueueSet()
    //Debug
    private var mDebugTextView: TextView? = null
    private var mDebugItemCount = 0




    class AnalysisResult(internal val mResults: ArrayList<Result>)

    override fun onCreate(savedInstanceState: Bundle?) {
        setContentView(contentViewLayoutId)
        cameraPreviewTextureView = updateCameraPreviewTextureView()
        mDebugTextView = findViewById(R.id.debugText)
        mResultTextView = findViewById(R.id.resultText)
        val buttonDrawBox = findViewById<Button>(R.id.drawResultsButton)
        buttonDrawBox.text = ("Drawing Results")
        buttonDrawBox.setOnClickListener(View.OnClickListener {
            if (mResultView!!.mDrawBoxes){
                buttonDrawBox.text = ("Not Drawing Results")
            } else {
                buttonDrawBox.text = ("Drawing Results")
            }
            mResultView!!.mDrawBoxes = !mResultView!!.mDrawBoxes
        })

        val buttonClearResults = findViewById<Button>(R.id.clearResultQueueButton)
        buttonClearResults.setOnClickListener(View.OnClickListener {
            mResultQueue = ResultsQueueSet()
            mResultTextView!!.text = "Reset Done"
        })

        super.onCreate(savedInstanceState)
    }

    private fun updateCameraPreviewTextureView(): TextureView {
        mResultView = findViewById(R.id.resultView)
        //Debug


        return (findViewById<View>(R.id.object_detection_texture_view_stub) as ViewStub)
            .inflate()
            .findViewById(R.id.object_detection_texture_view)
    }

    override fun applyToUiAnalyzeImageResult(result: AnalysisResult?, mElapsedTime: Long) {
        mResultView!!.setResults(result!!.mResults)
        //Debug
        val debugText = "# of obj identified: $mDebugItemCount"
        mDebugTextView!!.text = debugText
        mResultView!!.invalidate()
        for (r in result.mResults){
            mResultQueue.addResult(PrePostProcessor.mClasses[r.classIndex]!!,mElapsedTime)
        }
        mResultTextView!!.text = mResultQueue.getResultText()


    }

    private fun imgToBitmap(image: Image?): Bitmap {
        //Debug
        //Log.i("image height", image!!.height.toString())
        //Log.i("image width", image.width.toString())
        val planes = image!!.planes
        val yBuffer = planes[0].buffer
        val uBuffer = planes[1].buffer
        val vBuffer = planes[2].buffer

        val ySize = yBuffer.remaining()
        val uSize = uBuffer.remaining()
        val vSize = vBuffer.remaining()

        val nv21 = ByteArray(ySize + uSize + vSize)
        yBuffer[nv21, 0, ySize]
        vBuffer[nv21, ySize, vSize]
        uBuffer[nv21, ySize + vSize, uSize]

        val yuvImage = YuvImage(nv21, ImageFormat.NV21, image.width, image.height, null)
        val out = ByteArrayOutputStream()
        yuvImage.compressToJpeg(Rect(0, 0, yuvImage.width, yuvImage.height), 75, out)

        val imageBytes = out.toByteArray()
        return BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
    }

    @OptIn(ExperimentalGetImage::class)
    @WorkerThread
    override fun analyzeImage(image: ImageProxy?): AnalysisResult? {
        try {
            if (mModule == null) {
                mModule = LiteModuleLoader.load(
                    MainActivity.assetFilePath(
                        applicationContext,
                        MainActivity.MODEL_NAME
                    )
                )
            }
        } catch (e: IOException) {
            //Log.e("Object Detection", "Error reading assets", e)
            return null
        }
        var bitmap = imgToBitmap(image!!.image)
        val matrix = Matrix()
        matrix.postRotate(90.0f)
        bitmap = Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, bitmap.height, matrix, true)

        val resizedBitmap = Bitmap.createScaledBitmap(
            bitmap,
            PrePostProcessor.mInputWidth,
            PrePostProcessor.mInputHeight,
            true
        )

        val inputTensor = TensorImageUtils.bitmapToFloat32Tensor(
            resizedBitmap,
            PrePostProcessor.NO_MEAN_RGB,
            PrePostProcessor.NO_STD_RGB
        )
        var outputTensor: Tensor? = null
        if (MainActivity.MODEL_NAME === "old_best.torchscript" || MainActivity.MODEL_NAME === "NoLastLayer.torchscript.ptl") {

            val outputTuple = mModule!!.forward(IValue.from(inputTensor)).toTuple()
            outputTensor = outputTuple[0].toTensor()
            //Debug
            //Log.i("Output size",outputTensor.shape().toList().toString())
        } else {
            val outputTensorList = mModule!!.forward(IValue.from(inputTensor)).toTensorList()
            outputTensor = outputTensorList[0]
        }
        val outputs = outputTensor!!.dataAsFloatArray
        //Log.i("bitmap width", bitmap.getWidth().toString())
        //Log.i("bitmap height", bitmap.getHeight().toString())

        val imgScaleX = bitmap.width.toFloat() / PrePostProcessor.mInputWidth
        val imgScaleY = bitmap.height.toFloat() / PrePostProcessor.mInputHeight

        //Log.i("Orientation", String.valueOf(getWindowManager().getDefaultDisplay().getRotation()));
        val ivScaleX = mResultView!!.width.toFloat() / bitmap.width
        val ivScaleY = mResultView!!.height.toFloat() / bitmap.height
        //Log.i("mResultView width", mResultView!!.width.toString())
        //Log.i("mResultView height", mResultView!!.height.toString())
        val results =
            outputsToNMSPredictions(outputs, imgScaleX, imgScaleY, ivScaleX, ivScaleY, 0f, 0f)
        //Debug
        mDebugItemCount = results.size

        return AnalysisResult(results)
    }
}
