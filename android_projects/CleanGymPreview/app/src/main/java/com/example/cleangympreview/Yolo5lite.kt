package com.example.cleangympreview


import android.content.Context
import android.graphics.Bitmap
import android.graphics.RectF
import android.os.Build
import android.util.Log
import android.util.Size
import android.widget.Toast
import org.tensorflow.lite.DataType
import org.tensorflow.lite.Interpreter
import org.tensorflow.lite.gpu.CompatibilityList
import org.tensorflow.lite.gpu.GpuDelegate
import org.tensorflow.lite.nnapi.NnApiDelegate
import org.tensorflow.lite.support.common.FileUtil
import org.tensorflow.lite.support.common.ops.NormalizeOp
import org.tensorflow.lite.support.image.ImageProcessor
import org.tensorflow.lite.support.image.TensorImage
import org.tensorflow.lite.support.image.ops.ResizeOp
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer
import java.io.IOException
import java.nio.ByteBuffer
import java.util.Arrays
import java.util.PriorityQueue
import kotlin.math.max


class Yolo5lite {
    private val INPUTSIZE : Size = Size(640,640)
    private val outputSize : IntArray = intArrayOf(1,25200,10) //CHANGE the 10 when adding new class.txt

    private val DETECT_THRESHHOLD : Float = 0.25f
    private val IOU_THRESHOLD : Float = 0.45f
    private val IOU_CLASS_DUPLICATED_THRESHOLD : Float = 0.7f

    private val CLASSFILE = "classes.txt"

    private var bitmapHeight : Int = 0
    private var bitmapWidth : Int = 0
    private lateinit var modelFile : String
    private lateinit var tfliteInterpreter : Interpreter
    private var associatedAxisLabels: List<String> ? = null

    private var interpreterOptions  = Interpreter.Options()

    //getter and setter for model file
    fun getModelFile(): String{
        return this.modelFile
    }
    fun setModelFile(filePath:String) {
        this.modelFile = filePath
        Log.d("yolo5lite>>>", "model file set to:$filePath")
    }

    //getter for class file
    fun getClassFile(): String{return this.CLASSFILE}

    //Initialize model with addNNApiDelegate() and addGPUDelegate
    // GPU reference: https://www.tensorflow.org/lite/android/delegates/gpu
    // NNApi reference: https://www.tensorflow.org/lite/android/delegates/nnapi

    fun initModel(activity:Context){
        try{
            //load model
            Log.d("yolov5lite>>>", "loading model --- $modelFile")
            val tfliteModel: ByteBuffer = FileUtil.loadMappedFile(activity, modelFile)
            tfliteInterpreter = Interpreter(tfliteModel, interpreterOptions)
            Log.i("tfliteSupport", "Success reading model: $modelFile")
            //load label
            associatedAxisLabels = FileUtil.loadLabels(activity, CLASSFILE)
            //println(associatedAxisLabels.toString())
            Log.i("tfliteSupport", "Success reading label: $CLASSFILE")
        } catch (e:IOException){
            Log.e("tfliteSupport", "Error reading model or label: ", e)
            Toast.makeText(activity, "load model error: " + e.message, Toast.LENGTH_LONG).show()
        }
    }

    fun detect(bitmap: Bitmap):ArrayList<Recognition>{
        bitmapHeight = bitmap.height
        bitmapWidth = bitmap.width
        val resultArray = arrayListOf<Recognition>()
        val imageProcessor: ImageProcessor = ImageProcessor.Builder()
            .add(ResizeOp(INPUTSIZE.height,INPUTSIZE.width, ResizeOp.ResizeMethod.BILINEAR))
            .add(NormalizeOp(0f, 255f))
            .build()

        var inputTensor = TensorImage(DataType.FLOAT32)
        inputTensor.load(bitmap)
        inputTensor = imageProcessor.process(inputTensor)

        val probabilityBuffer : TensorBuffer = TensorBuffer.createFixedSize(outputSize,DataType.FLOAT32)

        //process
        Log.d("yolo5lite>>>",inputTensor.tensorBuffer.flatSize.toString() + " " + probabilityBuffer.flatSize.toString())
        tfliteInterpreter.run(inputTensor.buffer,probabilityBuffer.buffer)

        val result : FloatArray = probabilityBuffer.floatArray
        for(i in 0..<outputSize[2]){
            val gridStride: Int = i * outputSize[2]


            val x: Float = result.get(0 + gridStride) * bitmapWidth
            val y: Float = result.get(1 + gridStride) * bitmapHeight
            val w: Float = result.get(2 + gridStride) * bitmapWidth
            val h: Float = result.get(3 + gridStride) * bitmapHeight
            val xmin = max(0.0, x - w / 2.0).toInt()
            val ymin = max(0.0, y - h / 2.0).toInt()
            val xmax = bitmapWidth.coerceAtMost((x + w / 2.0).toInt())
            val ymax = bitmapHeight.coerceAtMost((y + h / 2.0).toInt())
            val confidence: Float = result.get(4 + gridStride)
            val classScores: FloatArray = Arrays.copyOfRange(result,5+gridStride,this.outputSize[2]+gridStride)
            var labelId = 0
            var maxLabelScores = 0f
            for (j in classScores.indices) {
                if (classScores[j] > maxLabelScores) {
                    maxLabelScores = classScores[j]
                    labelId = j
                }
            }
            val r = Recognition(
                labelId,
                "",
                maxLabelScores,
                confidence,
                RectF(xmin.toFloat(), ymin.toFloat(), xmax.toFloat(), ymax.toFloat())
            )
            resultArray.add(
                r
            )
        }
        //now we check for thresholds
        val nmsResult = nms(resultArray)
        // make sure that each box is only seeing one object
        val nmsFilterBoxDuplication = nmsAllClass(nmsResult)

        for (recognition : Recognition in nmsFilterBoxDuplication) {
            val labelId = recognition.labelId
            val labelName = associatedAxisLabels!![labelId]
            recognition.labelName = labelName
        }

        return resultArray
    }

    private fun nms(allRecognitions: ArrayList<Recognition>): ArrayList<Recognition> {
        val nmsRecognitions = ArrayList<Recognition>()
        // go through each categories
        for (i in 0 until outputSize[2] - 5) {
            // rank by labelScore
            val pq =
                PriorityQueue(
                    6300,
                    Comparator<Recognition> { l, r ->
                        // Intentionally reversed to put high confidence at the head of the queue.
                        r.confidence.compareTo(l.confidence)
                    })

            // filter by category, and filter pass the threshold
            for (j in 0 until allRecognitions.size) {
                if (allRecognitions[j].labelId == i && allRecognitions[j].confidence > DETECT_THRESHHOLD
                ) {
                    pq.add(allRecognitions[j])
                    //Log.i("tfliteSupport", allRecognitions[j].toString());
                }
            }
            // nms
            while (pq.size > 0) {
                val a = arrayOfNulls<Recognition>(pq.size)
                val detections = pq.toArray(a)
                val max = detections[0]!!
                nmsRecognitions.add(max)
                pq.clear()
                for (k in 1 until detections.size) {
                    val detection = detections[k]
                    if (boxIou(max.getLocation(), detection!!.getLocation()) < IOU_THRESHOLD) {
                        pq.add(detection)
                    }
                }
            }
        }
        return nmsRecognitions
    }

    private fun boxIou(a: RectF, b: RectF): Float {
        val intersection = boxIntersection(a,b)
        val union = boxUnion(a,b)
        if (union<=0) return 1f
        return intersection/union
    }

    private fun boxIntersection(a:RectF,b:RectF): Float{
        val maxLeft = if (a.left > b.left) a.left else b.left
        val maxTop = if (a.top > b.top) a.top else b.top
        val minRight = if (a.right < b.right) a.right else b.right
        val minBottom = if (a.bottom < b.bottom) a.bottom else b.bottom
        val w = minRight - maxLeft
        val h = minBottom - maxTop

        if (w < 0 || h < 0) return 0f
        val area = w * h
        return area
    }

    private fun boxUnion(a:RectF,b:RectF):Float{
        val i = boxIntersection(a, b)
        val u =
            (a.right - a.left) * (a.bottom - a.top) + (b.right - b.left) * (b.bottom - b.top) - i
        return u
    }

    private fun nmsAllClass(allRecognitions: ArrayList<Recognition>): ArrayList<Recognition> {
        val nmsRecognitions = ArrayList<Recognition>()

        val pq =
            PriorityQueue(
                6300,
                Comparator<Recognition> { l, r ->
                    // Intentionally reversed to put high confidence at the head of the queue.
                    r.confidence.compareTo(l.confidence)
                })

        for (j in 0 until allRecognitions.size) {
            if (allRecognitions[j].confidence > DETECT_THRESHHOLD) {
                pq.add(allRecognitions[j])
            }
        }

        while (pq.size > 0) {
            // 概率最大的先拿出来
            val a = arrayOfNulls<Recognition>(pq.size)
            val detections = pq.toArray(a)
            val max = detections[0]!!
            nmsRecognitions.add(max)
            pq.clear()

            for (k in 1 until detections.size) {
                val detection = detections[k]
                if (boxIou(
                        max.getLocation(),
                        detection!!.getLocation()
                    ) < IOU_CLASS_DUPLICATED_THRESHOLD
                ) {
                    pq.add(detection)
                }
            }
        }
        return nmsRecognitions
    }

    fun addGPUDelegate() {
        val compatibilityList = CompatibilityList()
        if (compatibilityList.isDelegateSupportedOnThisDevice) {
            val delegateOptions: GpuDelegate.Options = compatibilityList.bestOptionsForThisDevice
            val gpuDelegate = GpuDelegate()
            interpreterOptions.addDelegate(gpuDelegate)
            Log.i("tfliteSupport", "using gpu delegate.")
        } else {
            addThread(4)
        }
    }

    fun addNNApiDelegate() {
        val nnApiDelegate: NnApiDelegate
        // Initialize interpreter with NNAPI delegate for Android Pie or above
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            val nnApiOptions = NnApiDelegate.Options()
            nnApiOptions.setAllowFp16(true)
            nnApiOptions.setUseNnapiCpu(true)
            //ANEURALNETWORKS_PREFER_LOW_POWER：倾向于以最大限度减少电池消耗的方式执行。这种设置适合经常执行的编译。
            //ANEURALNETWORKS_PREFER_FAST_SINGLE_ANSWER：倾向于尽快返回单个答案，即使这会耗费更多电量。这是默认值。
            //ANEURALNETWORKS_PREFER_SUSTAINED_SPEED：倾向于最大限度地提高连续帧的吞吐量，例如，在处理来自相机的连续帧时。
            nnApiOptions.setExecutionPreference(NnApiDelegate.Options.EXECUTION_PREFERENCE_SUSTAINED_SPEED)
            nnApiDelegate = NnApiDelegate(nnApiOptions)
            //nnApiDelegate = NnApiDelegate()
            interpreterOptions.addDelegate(nnApiDelegate)
            Log.i("tfliteSupport", "using nnapi delegate.")
        }
    }
    private fun addThread(thread: Int) {
        interpreterOptions.setNumThreads(thread)
    }

}