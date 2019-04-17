import pyglet
import argparse


def takeArgs():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the list to sort')
    parser.add_argument('--algo',
                        help='specify which algorithm to use for sorting among\
               [bubble|insert|quick|merge], default bubble')
    parser.add_argument('--gui', action='store_true',
                        help='visualise the algorithm in GUI mode')
    args = parser.parse_args()
    return args


def returnSort():
    mode = args.algo
    num_lst = args.integers
    n = len(num_lst)
    if mode == 'insert':
        return insertSort(num_lst, n)
    elif mode == 'quick':
        return quickSort(num_lst, 0, n - 1)
    elif mode == 'merge':
        return mergeSort(num_lst)
    else:
        return bubbleSort(num_lst, n)


def bubbleSort(num_lst, n):
    global steps
    for i in range(n):
        for num in range(0, n-i-1):
            if num_lst[num] > num_lst[num+1]:
                num_lst[num], num_lst[num+1] = num_lst[num+1], num_lst[num]
                print(*num_lst)
                steps.append(tuple(num_lst))
    return num_lst


def insertSort(num_lst, n):
    global steps
    """loop through the list from 1 to length,
       for each element as key,
       check if the left elements is bigger,
       continue until reach smaller element,
       insert key before the last bigger element in the list
       print if there are any changes to the list
    """
    for num in range(1, n):
        no_change = True
        key = num_lst[num]
        move = num-1
        while move >= 0 and key < num_lst[move]:
            num_lst[move + 1] = num_lst[move]
            move -= 1
            no_change = False
        num_lst[move + 1] = key
        if not no_change:
            print(*num_lst)
            steps.append(tuple(num_lst))
    return num_lst


def partition(sample, start, end):
    global steps
    """take the last element as pivot,
       place smaller elements to the left
       and bigger elements to the right,
       then replace pivot with the first bigger element in the list
       """
    pivot = sample[end]
    index = start
    current = start
    pivots.append(end)
    print('P:', pivot)
    while current < end:
        if sample[current] < pivot:
            sample[current], sample[index] = sample[index], sample[current]
            index += 1
        current += 1
    sample[end], sample[index] = sample[index], sample[end]
    print(*sample)
    steps.append(tuple(sample))
    return index


def quickSort(num_lst, start, end):
    """break list into smaller lists
       with pivot as the last element of each list
       """
    if start < end:
        index = partition(num_lst, start, end)
        quickSort(num_lst, start, index - 1)
        quickSort(num_lst, index + 1, end)
    return num_lst


def mergeSort(num_lst):
    if len(num_lst) > 1:
        """break list in half to create new lists(L and R)
           continue until there are only 1 element left in list
           """
        half = len(num_lst)//2
        L = num_lst[:half]
        R = num_lst[half:]
        mergeSort(L)
        mergeSort(R)
        """place smaller elements first to new lists(L and R)
        """
        x = y = z = 0
        while x < len(L) and y < len(R):
            if L[x] < R[y]:
                num_lst[z] = L[x]
                x += 1
            else:
                num_lst[z] = R[y]
                y += 1
            z += 1
        """place elements to new list(L and R) if there're any left
        """
        while x < len(L):
            num_lst[z] = L[x]
            x += 1
            z += 1
        while y < len(R):
            num_lst[z] = R[y]
            y += 1
            z += 1
        print(*num_lst)
    return num_lst


if __name__ == '__main__':
    args = takeArgs()
    steps = [tuple(args.integers)]
    pivots = []
    num_lst = returnSort()
    if args.gui:
        c = 0
        '''--------------------TEXT-------------------------'''
        window = pyglet.window.Window(width=1440, height=1080)
        nstep = pyglet.text.Label('Steps: ' + str(len(steps) - 1),
                                  font_name='Times New Roman',
                                  font_size=25,
                                  x=window.width - 90, y=window.height - 100,
                                  anchor_x='center', anchor_y='center')
        if args.algo == 'quick':
            sort_kind = pyglet.text.Label('QUICK SORT',
                                     font_name='Times New Roman',
                                     font_size=50,
                                     x= 50, y= 80
                                     )
        '''-------------------SPRITE--------------------------'''
        background = pyglet.image.load('Pictures/bg.png')
        num = pyglet.image.load('Pictures/num.png')
        oha = pyglet.image.load('Pictures/aha.png')
        bg = pyglet.sprite.Sprite(img=background)
        aha = pyglet.sprite.Sprite(img=oha, x=window.width/2 - 600,
                                   y=window.height - 230)
        '''-------------------BATCH---------------------------'''
        def draw_squares():
            quantity = pyglet.graphics.Batch()
            elements = []
            sx = window.width / 2
            sy = window.height / 2 - 30
            for x in range(len(num_lst)):
                elements.append(pyglet.sprite.Sprite(img=num, x=sx, y=sy,
                                                     batch=quantity))
                if x < round(len(num_lst) / 2):
                    sx -= 85
                elif x == round(len(num_lst) / 2):
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
                                               y=f[i].y + 15, batch=labels))
            if args.algo == 'quick':
                if c >= 1:
                    label[pivots[c]].color = (255, 0, 0, 255)
                else:
                    label[-1].color = (255, 2 ,5, 255)
            return label, labels

        def repeat(c):
            elements, quantity = draw_squares()
            label, labels = label_draw(c, elements)
            quantity.draw()
            labels.draw()
        '''----------------KEYBOARD--------------------'''
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
        '''--------------ON-DRAW------------------------'''
        def on_draw(c):
            window.clear()
            bg.draw()
            aha.draw()
            repeat(c)
            if args.algo == 'quick':
                sort_kind.draw()
        pyglet.app.run()
