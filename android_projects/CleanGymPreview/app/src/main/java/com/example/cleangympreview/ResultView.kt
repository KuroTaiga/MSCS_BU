// Copyright (c) 2020 Facebook, Inc. and its affiliates.
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.
package com.example.cleangympreview

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.util.AttributeSet
import android.view.View
import java.lang.String

class ResultView : View {
    private var mPaintRectangle: Paint? = null
    private var mPaintText: Paint? = null
    private var mResults: ArrayList<Recognition>? = null

    constructor(context: Context?) : super(context)

    constructor(context: Context?, attrs: AttributeSet?) : super(context, attrs) {
        mPaintRectangle = Paint()
        mPaintRectangle!!.color = Color.YELLOW
        mPaintText = Paint()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        if (mResults == null) return
        for (result in mResults!!) {
            mPaintRectangle!!.strokeWidth = 5f
            mPaintRectangle!!.style = Paint.Style.STROKE
            var location = result.getLocation()
            canvas.drawRect(location, mPaintRectangle!!)

            val mPath = Path()
            val mRectF = RectF(
                location.left,
                location.top,
                location.right,
                location.bottom
            )
            mPath.addRect(mRectF, Path.Direction.CW)
            mPaintText!!.color = Color.MAGENTA
            canvas.drawPath(mPath, mPaintText!!)

            mPaintText!!.color = Color.WHITE
            mPaintText!!.strokeWidth = 0f
            mPaintText!!.style = Paint.Style.FILL
            mPaintText!!.textSize = 32f
            canvas.drawText(
                result.labelName+":"+result.confidence, location.left + TEXT_X, location.top + TEXT_Y,
                mPaintText!!
            )
        }
    }

    fun setResults(results: ArrayList<Recognition>?) {
        mResults = results
    }

    companion object {
        private const val TEXT_X = 40
        private const val TEXT_Y = 35
        private const val TEXT_WIDTH = 260
        private const val TEXT_HEIGHT = 50
    }
}