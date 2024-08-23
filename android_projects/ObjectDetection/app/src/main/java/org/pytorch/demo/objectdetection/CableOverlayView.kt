package org.pytorch.demo.objectdetection

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
//import android.graphics.Point
import org.opencv.core.Point
import android.util.AttributeSet
import android.view.View


class CableOverlayView (context: Context, attrs: AttributeSet?) : View(context, attrs) {
    private val paint = Paint().apply {
        color = Color.RED
        strokeWidth = 5f
    }
    var lines: List<Pair<Point, Point>> = emptyList()

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        lines.forEach { line ->
            canvas.drawLine(
                line.first.x.toFloat(), line.first.y.toFloat(),
                line.second.x.toFloat(), line.second.y.toFloat(),
                paint
            )
        }
    }
}
