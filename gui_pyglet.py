#!/usr/bin/env python3
import pyglet
from pyglet.window import mouse
from pyglet.window import key


def bubbleSort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        sorted = True
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                sorted = False
                steps.append(tuple(arr))  # for GUI
        if sorted:
            break
    return steps  # for GUI


def insertionSort(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        swap = False
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
            swap = True
        arr[j+1] = key
        if swap:
            steps.append(tuple(arr))  # for GUI
    return steps  # for GUI


def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot
    for j in range(low, high):
        # If current element is smaller than or
        # equal to pivot
        if arr[j] <= pivot:
            # increment index of smaller element
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)


# Function to do Quick sort
def quickSort(arr, low, high):
    steps = []
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)
        steps.append(tuple(arr))  # for GUI
        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)
    return steps  # for GUI


def mergeSort(arr):
    steps = []
    if len(arr) > 1:
        mid = len(arr)//2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves
        mergeSort(L)  # Sorting the first half
        mergeSort(R)  # Sorting the second half
        i = j = k = 0
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
        steps.append(tuple(arr))  # for GUI
    return steps  # for GUI


def handleAlgo(algo, arr):

    if algo.lower() == 'bubble':
        steps = bubbleSort(arr)
        title = 'Bubble Sort'
    elif algo.lower() == 'insert':
        steps = insertionSort(arr)
        title = 'Insertion Sort'
    elif algo.lower() == 'quick':
        steps = quickSort(arr, 0, len(arr)-1)
        title = 'Quick Sort'
    elif algo.lower() == 'merge':
        steps = mergeSort(arr)
        title = 'Merge Sort'
    return arr, title, steps


def gui_produce(algo, arr):
    sorted_list, title, steps = handleAlgo(algo, arr)
    window = pyglet.window.Window(width=1440, height=1080)

    '''--------------------TEXT-------------------------'''
    title_algo = pyglet.text.Label(title,
                                   font_name='Times New Roman',
                                   font_size=36,
                                   x=window.width//2,
                                   y=window.height//2 + 300,
                                   anchor_x='center', anchor_y='center')

    '''-------------------SPRITE--------------------------'''
    background = pyglet.image.load('pictures/background.jpg')
    bg = pyglet.sprite.Sprite(img=background)

    '''-------------------BATCH---------------------------'''
    def draw_squares():
        quantity = pyglet.graphics.Batch()
        elements = []
        sx = window.width / 2
        sy = window.height / 2 - 30
        for x in range(len(sorted_list)):
            elements.append(pyglet.sprite.Sprite(img=num, x=sx, y=sy,
                                                 batch=quantity))
            if x < round(len(sorted_list) / 2):
                sx -= 85
            elif x == round(len(sorted_list) / 2):
                sx = window.width / 2 + 85
            else:
                sx += 85
        return elements, quantity

    def label_draw(c, elements):
        labels = pyglet.graphics.Batch()
        label = []
        f = sorted(elements, key=lambda v: v.x)
        for i in range(len(f)):
            label.append(pyglet.text.Label(str(steps[c][i]),
                         font_name='Times New Roman',
                         font_size=35,
                         x=f[i].x + 15,
                         x=f[i].y + 15, batch=labels))
        return label, labels

    def repeat(c):
        elements, quantity = draw_squares()
        label, labels = label_draw(c, elements)
        quantity.draw()
        labels.draw()

    @window.event
    def on_draw():
        window.clear()
        title_algo.draw()
        bg.draw()
        repeat(c)

    @window.event
    def on_key_press(symbol, modifiers):
        global c
        if symbol == pyglet.window.key.DOWN:
            if c <= len(steps) - 1:
                on_draw(c)
                nstep.draw()
                c += 1
            else:
                exit()

    pyglet.app.run()
