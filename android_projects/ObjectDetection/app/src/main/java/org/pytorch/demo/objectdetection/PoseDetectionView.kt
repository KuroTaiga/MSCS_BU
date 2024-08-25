package org.pytorch.demo.objectdetection

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.util.AttributeSet
import android.view.View
import com.google.mlkit.vision.pose.PoseLandmark
import org.opencv.core.Point

class PoseDetectionView (context: Context, attrs: AttributeSet?) : View(context, attrs) {
    private var mLandmarks : MutableList<PoseLandmark>? = null
    private val paint = Paint().apply {
        color = Color.RED
        strokeWidth = 5f
    }
    var lines: List<Pair<Point, Point>> = emptyList()

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (mLandmarks == null) return
        val leftShoulderPointF  = mLandmarks!![PoseLandmark.LEFT_SHOULDER].position
        val rightShoulderPointF = mLandmarks!![PoseLandmark.RIGHT_SHOULDER].position
        val leftElbowPointF = mLandmarks!![PoseLandmark.LEFT_ELBOW].position
        val rightElbowPointF = mLandmarks!![PoseLandmark.RIGHT_ELBOW].position
        val leftWristPointF = mLandmarks!![PoseLandmark.LEFT_WRIST].position
        val rightWristPointF = mLandmarks!![PoseLandmark.RIGHT_WRIST].position

    }

    fun setLankMarks(landMarks: MutableList<PoseLandmark>?) {
        mLandmarks = landMarks
    }
}
