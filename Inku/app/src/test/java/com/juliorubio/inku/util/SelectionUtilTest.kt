package com.juliorubio.inku.util

import org.junit.Assert.assertEquals
import org.junit.Test

class SelectionUtilTest {

    @Test
    fun toggle_adds_when_absent() {
        val result = SelectionUtil.toggle(emptySet(), "Action")
        assertEquals(setOf("Action"), result)
    }

    @Test
    fun toggle_removes_when_present() {
        val result = SelectionUtil.toggle(setOf("Action"), "Action")
        assertEquals(emptySet<String>(), result)
    }
}
