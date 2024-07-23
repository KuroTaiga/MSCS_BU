// Copyright (c) 2020 Facebook, Inc. and its affiliates.
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.
package org.pytorch.demo.objectdetection

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.util.AttributeSet
import android.view.View

class ResultView : View {
    //TODO: Update to maintain a 3:4 width-height aspect ratio
    //private val aspectRatioWidth = 3
    //private val aspectRatioHeight = 4
    private var mPaintRectangle: Paint? = null
    private var mPaintText: Paint? = null
    private var mResults: ArrayList<Result>? = null
    var mDrawBoxes: Boolean = true


    constructor(context: Context?) : super(context)

    constructor(context: Context?, attrs: AttributeSet?) : super(context, attrs) {
        mPaintRectangle = Paint()
        mPaintRectangle!!.color = Color.YELLOW
        mPaintText = Paint()
    }


//    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
//        super.onMeasure(widthMeasureSpec, heightMeasureSpec)
//        val width = MeasureSpec.getSize(widthMeasureSpec)
//        val height = MeasureSpec.getSize(heightMeasureSpec)
//        if (aspectRatioWidth == 0 || aspectRatioHeight == 0) {
//            setMeasuredDimension(width, height)
//        } else {
//            if (width < height * aspectRatioWidth / aspectRatioHeight) {
//                setMeasuredDimension(width, width * aspectRatioHeight / aspectRatioWidth)
//            } else {
//                setMeasuredDimension(height * aspectRatioWidth / aspectRatioHeight, height)
//            }
//        }
//    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        //no results don't draw anything
        if (mResults == null) return
        var textOffSet = 0
        for (result in mResults!!) {
            if (mDrawBoxes) draw_result_boxes(canvas, result)

            textOffSet += 1
        }
    }

    private fun draw_result_boxes(
        canvas: Canvas,
        result: Result
    ) {
        mPaintRectangle!!.strokeWidth = 5f
        mPaintRectangle!!.style = Paint.Style.STROKE
        canvas.drawRect(result.rect, mPaintRectangle!!)

        val mPath = Path()
        val mRectF = RectF(
            result.rect.left.toFloat(),
            result.rect.top.toFloat(),
            (result.rect.left + TEXT_WIDTH).toFloat(),
            (result.rect.top + TEXT_HEIGHT).toFloat()
        )
        mPath.addRect(mRectF, Path.Direction.CW)
        mPaintText!!.color = Color.MAGENTA
        canvas.drawPath(mPath, mPaintText!!)

        mPaintText!!.color = Color.WHITE
        mPaintText!!.strokeWidth = 0f
        mPaintText!!.style = Paint.Style.FILL
        mPaintText!!.textSize = 32f
        canvas.drawText(
            String.format(
                "%s %.2f",
                PrePostProcessor.mClasses[result.classIndex],
                result.score
            ),
            (result.rect.left + TEXT_X).toFloat(),
            (result.rect.top + TEXT_Y).toFloat(),
            mPaintText!!
        )
    }

    fun setResults(results: ArrayList<Result>?) {
        mResults = results
    }

    companion object {
        private const val TEXT_X = 40
        private const val TEXT_Y = 35
        private const val TEXT_WIDTH = 260
        private const val TEXT_HEIGHT = 50
    }
}
