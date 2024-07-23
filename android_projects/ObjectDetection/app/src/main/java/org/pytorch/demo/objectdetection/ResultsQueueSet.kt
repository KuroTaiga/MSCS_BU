package org.pytorch.demo.objectdetection

import org.pytorch.demo.objectdetection.Result
import java.util.PriorityQueue

data class ResultPairs(val name: String, val time: Long)

class ResultsQueueSet{
    private val queue: PriorityQueue<ResultPairs> = PriorityQueue(compareByDescending{it.time})
    private val resultMap: MutableMap<String,ResultPairs> = mutableMapOf()

    fun addResult(name: String, time: Long){
        var oldTime : Long = 0
        if (resultMap.containsKey(name)){
            queue.remove(resultMap[name])
            oldTime = resultMap[name]!!.time
        }
        val newResult = ResultPairs(name,time+oldTime)
        queue.add(newResult)
        resultMap[name] = newResult
    }

    fun removeResult(name: String) {
        if (resultMap.containsKey(name)) {
            queue.remove(resultMap[name])
            resultMap.remove(name)
        }
    }

    fun getResultText() : String{
        // this function formats the stored info and put it in a ready to print string with new line for each class
        val resultText  = StringBuilder()
        val tempQueue = PriorityQueue(queue)
        while(tempQueue.isNotEmpty()){
            val resultPair = tempQueue.poll()
            resultText.append("${resultPair.name}: ${resultPair.time}\n")
        }
        return resultText.toString().trim()
    }

    fun getResultTime(name :String) : Long{
        return resultMap[name]!!.time
    }

    fun peek(): ResultPairs? {
        return queue.peek()
    }

    fun poll(): ResultPairs? {
        val item = queue.poll()
        if (item != null) {
            resultMap.remove(item.name)
        }
        return item
    }

    fun getSize(): Int {
        return queue.size
    }

    fun isEmpty(): Boolean {
        return queue.isEmpty()
    }
}
