package org.pytorch.demo.objectdetection

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.PointF
import android.util.AttributeSet
import android.util.Log
import android.view.View
import com.google.mlkit.vision.pose.Pose
import com.google.mlkit.vision.pose.PoseLandmark
import org.opencv.core.Point

class PoseDetectionView : View{
    private var mPaintPoint : Paint? = null

    private var mLandmarks : MutableList<PoseLandmark>? = null
    private val mPaintPoints : List<Int> = listOf(
        PoseLandmark.LEFT_WRIST, PoseLandmark.RIGHT_WRIST,
        PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER,
        PoseLandmark.LEFT_HIP,PoseLandmark.RIGHT_HIP,
        PoseLandmark.LEFT_KNEE, PoseLandmark.RIGHT_KNEE,
        PoseLandmark.LEFT_ANKLE, PoseLandmark.RIGHT_ANKLE)
    constructor(context: Context?) : super(context)

    constructor(context: Context?, attrs: AttributeSet?) : super(context, attrs) {
        mPaintPoint = Paint()
        mPaintPoint!!.color = Color.RED
    }
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (mLandmarks == null) return
        if (mLandmarks!!.size == 0) return
//        for (pInt in mPaintPoints){
//            val currPointF = mLandmarks!![pInt].position
//            mPaintPoint = Paint()
//            mPaintPoint!!.color = Color.RED
//            canvas.drawCircle(currPointF.x,currPointF.y,10.0f,mPaintPoint!!)
//        }
        for (points in mLandmarks!!){
            val currPointF = points.position
            Log.i("x",currPointF.x.toString())
            Log.i("y",currPointF.y.toString())
            canvas.drawCircle(currPointF.x,currPointF.y,5f,mPaintPoint!!)
        }
        Log.i("Landmark size", mLandmarks!!.size.toString())
        drawFigure(canvas)


    }

    private fun drawFigure(canvas:Canvas){
        Log.i("DrawFigure", "Drawing figure based on landmark")
        val leftShoulderPointF  = mLandmarks!![PoseLandmark.LEFT_SHOULDER].position
        val rightShoulderPointF = mLandmarks!![PoseLandmark.RIGHT_SHOULDER].position
        val leftElbowPointF = mLandmarks!![PoseLandmark.LEFT_ELBOW].position
        val rightElbowPointF = mLandmarks!![PoseLandmark.RIGHT_ELBOW].position
        val leftWristPointF = mLandmarks!![PoseLandmark.LEFT_WRIST].position
        val rightWristPointF = mLandmarks!![PoseLandmark.RIGHT_WRIST].position
        val leftHipPointF = mLandmarks!![PoseLandmark.LEFT_HIP].position
        val rightHipPointF = mLandmarks!![PoseLandmark.RIGHT_HIP].position
        val leftKneePointF = mLandmarks!![PoseLandmark.LEFT_KNEE].position
        val rightKneePointF = mLandmarks!![PoseLandmark.RIGHT_KNEE].position
        val leftAnklePointF = mLandmarks!![PoseLandmark.LEFT_ANKLE].position
        val rightAnklePointF = mLandmarks!![PoseLandmark.RIGHT_ANKLE].position

        canvas.drawLine(leftShoulderPointF.x,leftShoulderPointF.y,rightShoulderPointF.x,rightShoulderPointF.y,mPaintPoint!!)
        canvas.drawLine(leftShoulderPointF.x,leftShoulderPointF.y,leftHipPointF.x,leftHipPointF.y,mPaintPoint!!)
        canvas.drawLine(leftShoulderPointF.x,leftShoulderPointF.y,leftElbowPointF.x,leftElbowPointF.y,mPaintPoint!!)
        canvas.drawLine(rightShoulderPointF.x,rightShoulderPointF.y,rightElbowPointF.x,rightElbowPointF.y,mPaintPoint!!)
        canvas.drawLine(rightShoulderPointF.x,rightShoulderPointF.y,rightHipPointF.x,rightHipPointF.y,mPaintPoint!!)
        canvas.drawLine(leftElbowPointF.x,leftElbowPointF.y,leftWristPointF.x,leftWristPointF.y,mPaintPoint!!)
        canvas.drawLine(rightElbowPointF.x,rightElbowPointF.y,rightWristPointF.x,rightWristPointF.y,mPaintPoint!!)

        canvas.drawLine(leftHipPointF.x,leftHipPointF.y,rightHipPointF.x,rightHipPointF.y,mPaintPoint!!)
        canvas.drawLine(leftHipPointF.x,leftHipPointF.y,leftKneePointF.x,leftKneePointF.y,mPaintPoint!!)
        canvas.drawLine(rightHipPointF.x,rightHipPointF.y,rightKneePointF.x,rightKneePointF.y,mPaintPoint!!)

        canvas.drawLine(leftKneePointF.x,leftKneePointF.y,leftAnklePointF.x,leftAnklePointF.y,mPaintPoint!!)
        canvas.drawLine(rightKneePointF.x,rightKneePointF.y,rightAnklePointF.x,rightAnklePointF.y,mPaintPoint!!)



    }

    fun setLankMarks(landMarks: MutableList<PoseLandmark>?) {
        mLandmarks = landMarks
    }
}
