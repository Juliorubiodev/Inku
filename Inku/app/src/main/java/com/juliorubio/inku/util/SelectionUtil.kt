package com.juliorubio.inku.util

object SelectionUtil {
    /**
     * Alterna la pertenencia de [item] en el conjunto [selected].
     * Si está, lo quita; si no está, lo añade.
     */
    fun toggle(selected: Set<String>, item: String): Set<String> =
        if (item in selected) selected - item else selected + item
}
