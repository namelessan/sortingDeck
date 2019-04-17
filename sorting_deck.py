#!/usr/bin/env python3
import argparse
# from gui_pyglet import *


def getArgs():
    """config the usage of rsync and arguments"""
    parser = argparse.ArgumentParser(prog='sorting_deck.py')
    parser.add_argument('integers', metavar='N', type=int,
                        nargs='+', help='an integer for the\
                        list to sort')
    parser.add_argument('--algo', action='store', default='bubble',
                        help='specify which algorithm to use for\
                        sorting among\n[bubble | insert | quick | merge],'
                        ' default bubble')
    parser.add_argument('--gui', action='store_true', default=False,
                        help='visualise the algorithm in GUI mode')
    return parser.parse_args()


def bubbleSort(arr):
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
                print(' '.join(map(str, arr)))  # for Sentinel
        if sorted:
            break


def insertionSort(arr):
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
            print(' '.join(map(str, arr)))  # for Sentinel


def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot
    print('P:', pivot)  # for sentinel
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
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)
        print(' '.join(map(str, arr)))  # for Sentinel
        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)


def mergeSort(arr):
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
        print(' '.join(map(str, arr)))  # for Sentinel


def handleAlgo(algo, arr):
    if algo.lower() == 'bubble':
        bubbleSort(arr)
    elif algo.lower() == 'insert':
        insertionSort(arr)
    elif algo.lower() == 'quick':
        quickSort(arr, 0, len(arr)-1)
    elif algo.lower() == 'merge':
        mergeSort(arr)
    return arr


# Driver code to test above
args = getArgs()
arr = args.integers
algo = args.algo
gui = args.gui

if gui:
    if len(arr) > 15:
        print('Input too large')
    else:
        pass
        # gui_produce(algo, arr)
else:
    handleAlgo(algo, arr)
