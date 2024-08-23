package org.pytorch.demo.objectdetection

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.util.AttributeSet
import android.view.View

class LineView : View {
    private var mLines: Paint? = null
    private var mPaintText: Paint? = null
    private var mResults: ArrayList<Result>? = null
    var mDrawBoxes: Boolean = true


    constructor(context: Context?) : super(context)

    constructor(context: Context?, attrs: AttributeSet?) : super(context, attrs) {
        mLines = Paint()
        mLines!!.color = Color.YELLOW
        mPaintText = Paint()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        //no results don't draw anything
        if (mResults == null) return
        
    }
}