package com.example.cleangympreview

import android.graphics.RectF

class Recognition(
    /**
     * Display name for the recognition.
     */
    var labelId: Int, var labelName: String?, var labelScore: Float,
    /**
     * A sortable score for how good the recognition is relative to others. Higher should be better.
     */
    var confidence: Float,
    /**
     * Optional location within the source image for the location of the recognized object.
     */
    private var location: RectF)
{
    fun setLabelID(idVal : Int){
        this.labelId = idVal
    }

    override fun toString(): String {
        var resultString = ""

        resultString += "$labelId "

        if (labelName != null) {
            resultString += "$labelName "
        }

        if (confidence != null) {
            resultString += String.format("(%.1f%%) ", confidence!! * 100.0f)
        }

        if (location != null) {
            resultString += location.toString() + " "
        }

        return resultString.trim { it <= ' ' }
    }

    fun getLocation(): RectF {
        return this.location
    }


}