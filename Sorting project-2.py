import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SortingAlgorithms:
    #class containing all sorting algorithm implementations
    
    @staticmethod
    def bubble_sort(arr):
        # bubble sort implementation with adjacent element comparison and swapping
        n = len(arr)
        for i in range(n):
            for j in range(n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    @staticmethod
    def insertion_sort(arr):
        # insertion sort that builds sorted array one element at a time
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >= 0 and arr[j] > key:
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

    @staticmethod
    def merge_sort(arr):
        # merge sort using divide and conquer approach
        if len(arr) > 1:
            mid = len(arr)//2
            left = arr[:mid]
            right = arr[mid:]
            SortingAlgorithms.merge_sort(left)
            SortingAlgorithms.merge_sort(right)
            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
        return arr

    @staticmethod
    def quick_sort(arr):
        # quick sort with middle element as pivot
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr)//2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return SortingAlgorithms.quick_sort(left) + middle + SortingAlgorithms.quick_sort(right)

    @staticmethod
    def counting_sort(arr):
        # counting sort for integer lists with known range
        if not arr:
            return arr
        max_val = max(arr)
        min_val = min(arr)
        count = [0] * (max_val - min_val + 1)
        for num in arr:
            count[num - min_val] += 1
        sorted_arr = []
        for i in range(len(count)):
            sorted_arr.extend([i + min_val] * count[i])
        return sorted_arr

class LinkedList:
    #class implementing singly linked list functionality
    
    class Node:
        # nested class for linked list nodes
        def __init__(self, data):
            self.data = data
            self.next = None
    
    def __init__(self):
        # initialize empty linked list
        self.head = None
        self.size = 0
    
    def insert_at_head(self, data):
        # insert new node at the beginning of the list
        new_node = self.Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def load_from_file(self, filename):
        # load list data from file (one number per line)
        try:
            with open(filename, 'r') as file:
                for line in file:
                    self.insert_at_head(int(line.strip()))
            return True
        except Exception as e:
            print(f"error loading file: {e}")
            return False
    
    def minimum(self):
        # find minimum value in the list
        if not self.head:
            return None
        current = self.head
        min_val = current.data
        while current:
            if current.data < min_val:
                min_val = current.data
            current = current.next
        return min_val
    
    def maximum(self):
        # find maximum value in the list
        if not self.head:
            return None
        current = self.head
        max_val = current.data
        while current:
            if current.data > max_val:
                max_val = current.data
            current = current.next
        return max_val
    
    def search(self, value):
        # search for value in the list
        current = self.head
        while current:
            if current.data == value:
                return current
            current = current.next
        return None
    
    def predecessor(self, value):
        # find predecessor of given value
        if not self.head or self.head.data == value:
            return None
        prev = None
        current = self.head
        while current and current.data != value:
            prev = current
            current = current.next
        if not current:
            return None
        return prev.data if prev else None
    
    def successor(self, value):
        # find successor of given value
        node = self.search(value)
        if not node or not node.next:
            return None
        return node.next.data
    
    def to_list(self):
        # convert linked list to python list
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
class AlgorithmPlatform:
    #main application class for the algorithm platform
    
    def __init__(self, root):
        # initialize main application window
        self.root = root
        self.root.title("Algorithm Platform")
        self.root.geometry("900x700")
        self.linked_list = LinkedList()  # create linked list instance
        self.bst = BinarySearchTree()  # create BST instance
        self.setup_interface()  # this calls create_bst_tab() which needs self.bst
    
    def setup_interface(self):
        # set up the main interface components
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # create all tabs
        self.create_sorting_tab()
        self.create_performance_tab()
        self.create_linked_list_tab()
        self.create_bst_tab()
        self.create_hash_table_tab()
        
    def generate_random_numbers(self):
        # generate random numbers for sorting
        count = random.randint(5, 20)
        numbers = [random.randint(1, 100) for _ in range(count)]
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, ", ".join(map(str, numbers)))
    
    def create_sorting_tab(self):
        # create sorting algorithms tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Sorting Algorithms")
        
        # algorithm selection
        algo_frame = ttk.LabelFrame(tab, text="select algorithm", padding=10)
        algo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.sort_algo = tk.StringVar(value="Bubble Sort")
        algorithms = ["Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Counting Sort"]
        
        for algo in algorithms:
            ttk.Radiobutton(algo_frame, text=algo, variable=self.sort_algo, value=algo).pack(anchor=tk.W)
        
        # input section
        input_frame = ttk.LabelFrame(tab, text="input numbers", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(fill=tk.X, pady=5)
        
        ttk.Button(input_frame, text="generate random numbers", command=self.generate_random_numbers).pack(pady=5)
        
        # output section
        output_frame = ttk.LabelFrame(tab, text="results", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.output_text = tk.Text(output_frame)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # action buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="sort", command=self.run_sort).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="clear", command=self.clear_results).pack(side=tk.LEFT)
    
    def create_performance_tab(self):
        # create performance testing tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Performance Testing")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="test settings", padding=10)
        settings_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Label(settings_frame, text="input sizes (comma separated):").pack(anchor=tk.W)
        self.sizes_entry = ttk.Entry(settings_frame)
        self.sizes_entry.pack(fill=tk.X, pady=5)
        self.sizes_entry.insert(0, "10,100,1000,10000")
        
        ttk.Label(settings_frame, text="number of test runs:").pack(anchor=tk.W)
        self.runs_entry = ttk.Entry(settings_frame)
        self.runs_entry.pack(fill=tk.X, pady=5)
        self.runs_entry.insert(0, "10")
        
        ttk.Label(settings_frame, text="select algorithms to test:").pack(anchor=tk.W)
        
        self.algo_vars = {
            "Bubble Sort": tk.BooleanVar(value=True),
            "Insertion Sort": tk.BooleanVar(value=True),
            "Merge Sort": tk.BooleanVar(value=True),
            "Quick Sort": tk.BooleanVar(value=True),
            "Counting Sort": tk.BooleanVar(value=True)
        }
        
        algo_frame = ttk.Frame(settings_frame)
        algo_frame.pack(fill=tk.X)
        
        for algo, var in self.algo_vars.items():
            ttk.Checkbutton(algo_frame, text=algo, variable=var).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(settings_frame, text="run performance test", command=self.run_performance_test).pack(pady=10)
        
        # results frame
        results_frame = ttk.LabelFrame(main_frame, text="test results", padding=10)
        results_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.results_text = tk.Text(results_frame, height=8)
        self.results_text.pack(fill=tk.X, pady=(0, 10))
        
        self.figure = plt.figure(figsize=(8, 4), dpi=100)
        self.figure.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.9)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=results_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # add navigation toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(self.canvas, results_frame)
        toolbar.update()
    


    def sort_linked_list(self):
        # sort the linked list using selected algorithm
        if not self.linked_list.head:
            messagebox.showinfo("info", "linked list is empty")
            return
        
        # convert linked list to regular list for sorting
        lst = self.linked_list.to_list()
        algorithm = self.ll_sort_algo.get()
        
        start_time = time.time()
        
        if algorithm == "Bubble Sort":
            sorted_list = SortingAlgorithms.bubble_sort(lst.copy())
        elif algorithm == "Insertion Sort":
            sorted_list = SortingAlgorithms.insertion_sort(lst.copy())
        elif algorithm == "Merge Sort":
            sorted_list = SortingAlgorithms.merge_sort(lst.copy())
        elif algorithm == "Quick Sort":
            sorted_list = SortingAlgorithms.quick_sort(lst.copy())
        elif algorithm == "Counting Sort":
            sorted_list = SortingAlgorithms.counting_sort(lst.copy())
        
        time_taken = time.time() - start_time
        
        # rebuild linked list from sorted list
        self.linked_list = LinkedList()
        for num in reversed(sorted_list):  # insert at head reverses order
            self.linked_list.insert_at_head(num)
        
        self.update_linked_list_display()
        messagebox.showinfo("sort complete", 
                          f"list sorted with {algorithm}\n"
                          f"time taken: {time_taken:.6f} seconds")
    
    
    def run_sort(self):
        # execute selected sorting algorithm
        try:
            numbers = [int(num.strip()) for num in self.input_entry.get().split(",")]
        except ValueError:
            messagebox.showerror("error", "please enter valid numbers separated by commas")
            return
        
        algorithm = self.sort_algo.get()
        original = numbers.copy()
        
        start_time = time.time()
        
        if algorithm == "Bubble Sort":
            result = SortingAlgorithms.bubble_sort(numbers.copy())
        elif algorithm == "Insertion Sort":
            result = SortingAlgorithms.insertion_sort(numbers.copy())
        elif algorithm == "Merge Sort":
            result = SortingAlgorithms.merge_sort(numbers.copy())
        elif algorithm == "Quick Sort":
            result = SortingAlgorithms.quick_sort(numbers.copy())
        elif algorithm == "Counting Sort":
            result = SortingAlgorithms.counting_sort(numbers.copy())
        
        time_taken = time.time() - start_time
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"algorithm: {algorithm}\n")
        self.output_text.insert(tk.END, f"original: {original}\n")
        self.output_text.insert(tk.END, f"sorted: {result}\n")
        self.output_text.insert(tk.END, f"time: {time_taken:.6f} seconds\n")
        
    def create_linked_list_tab(self):
        # create linked list operations tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Linked List")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # input section
        input_frame = ttk.LabelFrame(main_frame, text="linked list operations", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # file loading
        file_frame = ttk.Frame(input_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_frame, text="load from file", command=self.load_linked_list_from_file).pack(side=tk.LEFT)
        
        # manual input
        manual_frame = ttk.Frame(input_frame)
        manual_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(manual_frame, text="enter value:").pack(side=tk.LEFT)
        self.ll_input_entry = ttk.Entry(manual_frame)
        self.ll_input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(manual_frame, text="insert at head", command=self.insert_to_linked_list).pack(side=tk.LEFT)
        
        # operations
        ops_frame = ttk.Frame(input_frame)
        ops_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ops_frame, text="search value:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(ops_frame, width=10)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(ops_frame, text="search", command=self.search_linked_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(ops_frame, text="find min", command=self.find_min).pack(side=tk.LEFT, padx=5)
        ttk.Button(ops_frame, text="find max", command=self.find_max).pack(side=tk.LEFT, padx=5)
        
        # predecessor/successor
        ps_frame = ttk.Frame(input_frame)
        ps_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ps_frame, text="node value:").pack(side=tk.LEFT)
        self.ps_entry = ttk.Entry(ps_frame, width=10)
        self.ps_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(ps_frame, text="predecessor", command=self.find_predecessor).pack(side=tk.LEFT, padx=5)
        ttk.Button(ps_frame, text="successor", command=self.find_successor).pack(side=tk.LEFT, padx=5)
        
        # sorting section
        sort_frame = ttk.LabelFrame(input_frame, text="sort linked list", padding=5)
        sort_frame.pack(fill=tk.X, pady=5)
        
        self.ll_sort_algo = tk.StringVar(value="Bubble Sort")
        algorithms = ["Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Counting Sort"]
        
        for algo in algorithms:
            ttk.Radiobutton(sort_frame, text=algo, variable=self.ll_sort_algo, value=algo).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(sort_frame, text="sort list", command=self.sort_linked_list).pack(side=tk.LEFT, padx=5)
        
        # display section
        display_frame = ttk.LabelFrame(main_frame, text="linked list contents", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.ll_display = tk.Text(display_frame)
        self.ll_display.pack(fill=tk.BOTH, expand=True)
        
        # update display initially
        self.update_linked_list_display()
    
    def clear_results(self):
        # clear sorting results display
        self.output_text.delete(1.0, tk.END)
    
    def run_performance_test(self):
        # run performance comparison of sorting algorithms
        try:
            sizes = [int(size.strip()) for size in self.sizes_entry.get().split(",")]
            runs = int(self.runs_entry.get())
        except ValueError:
            messagebox.showerror("error", "please enter valid sizes and runs")
            return
        
        selected_algos = [algo for algo, var in self.algo_vars.items() if var.get()]
        if not selected_algos:
            messagebox.showerror("error", "please select at least one algorithm")
            return
        
        results = {algo: [] for algo in selected_algos}
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "running performance tests...\n")
        self.root.update()
        
        for size in sizes:
            self.results_text.insert(tk.END, f"\ntesting size {size}:\n")
            
            for algo in selected_algos:
                times = []
                for _ in range(runs):
                    test_data = [random.randint(1, size*10) for _ in range(size)]
                    sort_func = getattr(SortingAlgorithms, algo.lower().replace(" ", "_"))
                    start = time.time()
                    sort_func(test_data.copy())
                    times.append(time.time() - start)
                
                avg_time = sum(times) / runs
                results[algo].append(avg_time)
                self.results_text.insert(tk.END, f"{algo}: {avg_time:.6f} sec\n")
                self.root.update()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        for algo in selected_algos:
            ax.plot(sizes, results[algo], label=algo, marker='o')
        
        ax.set_xlabel('input size')
        ax.set_ylabel('average time (seconds)')
        ax.set_title('sorting algorithm performance')
        ax.legend()
        ax.grid(True)
        
        if max(sizes) / min(sizes) > 100:
            ax.set_xscale('log')
            ax.set_yscale('log')
        
        self.canvas.draw()
    
    def load_linked_list_from_file(self):
        # load linked list data from file
        filename = filedialog.askopenfilename(title="select file", filetypes=[("text files", "*.txt")])
        if filename:
            self.linked_list = LinkedList()  # clear current list
            if self.linked_list.load_from_file(filename):
                self.update_linked_list_display()
                messagebox.showinfo("success", "linked list loaded from file")
            else:
                messagebox.showerror("error", "failed to load linked list from file")
    
    def insert_to_linked_list(self):
        # insert value at head of linked list
        value = int(self.ll_input_entry.get())
        self.linked_list.insert_at_head(value)
        self.ll_input_entry.delete(0, tk.END)
        self.update_linked_list_display()

    def search_linked_list(self):
        # search for value in linked list
        try:
            value = int(self.search_entry.get())
            node = self.linked_list.search(value)
            if node:
                messagebox.showinfo("search result", f"value {value} found in linked list")
            else:
                messagebox.showinfo("search result", f"value {value} not found in linked list")
        except ValueError:
            messagebox.showerror("error", "please enter a valid integer")
    
    def find_min(self):
        # find minimum value in linked list
        min_val = self.linked_list.minimum()
        if min_val is not None:
            messagebox.showinfo("minimum", f"minimum value: {min_val}")
        else:
            messagebox.showinfo("minimum", "linked list is empty")
    
    def find_max(self):
        # find maximum value in linked list
        max_val = self.linked_list.maximum()
        if max_val is not None:
            messagebox.showinfo("maximum", f"maximum value: {max_val}")
        else:
            messagebox.showinfo("maximum", "linked list is empty")
    
    def find_predecessor(self):
        # find predecessor of value in linked list
        try:
            value = int(self.ps_entry.get())
            pred = self.linked_list.predecessor(value)
            if pred is not None:
                messagebox.showinfo("predecessor", f"predecessor of {value}: {pred}")
            else:
                messagebox.showinfo("predecessor", f"no predecessor found for {value}")
        except ValueError:
            messagebox.showerror("error", "please enter a valid integer")
    
    def find_successor(self):
        # find successor of value in linked list
        try:
            value = int(self.ps_entry.get())
            succ = self.linked_list.successor(value)
            if succ is not None:
                messagebox.showinfo("successor", f"successor of {value}: {succ}")
            else:
                messagebox.showinfo("successor", f"no successor found for {value}")
        except ValueError:
            messagebox.showerror("error", "please enter a valid integer")
    
    def update_linked_list_display(self):
        # update linked list display with current contents
        self.ll_display.delete(1.0, tk.END)
        ll_contents = self.linked_list.to_list()
        if ll_contents:
            self.ll_display.insert(tk.END, "List contents:\n")
            self.ll_display.insert(tk.END, ",".join(map(str, ll_contents)))
            
    def create_bst_tab(self):
        # create binary search tree operations tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Binary Search Tree")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # input section
        input_frame = ttk.LabelFrame(main_frame, text="BST operations", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # file loading
        file_frame = ttk.Frame(input_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_frame, text="load from file", command=self.load_bst_from_file).pack(side=tk.LEFT)
        ttk.Button(file_frame, text="clear BST", command=self.clear_bst).pack(side=tk.LEFT, padx=5)
        
        # manual input
        manual_frame = ttk.Frame(input_frame)
        manual_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(manual_frame, text="enter value:").pack(side=tk.LEFT)
        self.bst_input_entry = ttk.Entry(manual_frame)
        self.bst_input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(manual_frame, text="insert", command=self.insert_to_bst).pack(side=tk.LEFT, padx=2)
        ttk.Button(manual_frame, text="delete", command=self.delete_from_bst).pack(side=tk.LEFT, padx=2)
        
        # operations
        ops_frame = ttk.Frame(input_frame)
        ops_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ops_frame, text="search value:").pack(side=tk.LEFT)
        self.bst_search_entry = ttk.Entry(ops_frame, width=10)
        self.bst_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(ops_frame, text="search", command=self.search_bst).pack(side=tk.LEFT, padx=5)
        ttk.Button(ops_frame, text="find min", command=self.find_bst_min).pack(side=tk.LEFT, padx=5)
        ttk.Button(ops_frame, text="find max", command=self.find_bst_max).pack(side=tk.LEFT, padx=5)
        
        # predecessor/successor
        ps_frame = ttk.Frame(input_frame)
        ps_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ps_frame, text="node value:").pack(side=tk.LEFT)
        self.bst_ps_entry = ttk.Entry(ps_frame, width=10)
        self.bst_ps_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(ps_frame, text="predecessor", command=self.find_bst_predecessor).pack(side=tk.LEFT, padx=5)
        ttk.Button(ps_frame, text="successor", command=self.find_bst_successor).pack(side=tk.LEFT, padx=5)
        
        # traversal options
        traversal_frame = ttk.LabelFrame(input_frame, text="tree traversal", padding=5)
        traversal_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(traversal_frame, text="inorder", command=self.show_inorder).pack(side=tk.LEFT, padx=5)
        ttk.Button(traversal_frame, text="preorder", command=self.show_preorder).pack(side=tk.LEFT, padx=5)
        ttk.Button(traversal_frame, text="postorder", command=self.show_postorder).pack(side=tk.LEFT, padx=5)
        ttk.Button(traversal_frame, text="visualize tree", command=self.visualize_bst).pack(side=tk.LEFT, padx=5)
        
        # display section
        display_frame = ttk.LabelFrame(main_frame, text="BST contents", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.bst_display = tk.Text(display_frame)
        self.bst_display.pack(fill=tk.BOTH, expand=True)
        
        # update display initially
        self.update_bst_display()
    
    def load_bst_from_file(self):
        # load BST data from file
        filename = filedialog.askopenfilename(title="select file", filetypes=[("text files", "*.txt")])
        if filename:
            self.bst = BinarySearchTree()  # clear current BST
            if self.bst.load_from_file(filename):
                self.update_bst_display()
                messagebox.showinfo("success", "BST loaded from file")
            else:
                messagebox.showerror("error", "failed to load BST from file")
    
    def clear_bst(self):
        # clear the BST
        self.bst = BinarySearchTree()
        self.update_bst_display()
        messagebox.showinfo("success", "BST cleared")
    
    def insert_to_bst(self):
        # insert value into BST
        try:
            value = int(self.bst_input_entry.get())
            self.bst.insert(value)
            self.bst_input_entry.delete(0, tk.END)
            self.update_bst_display()
        except ValueError:
            messagebox.showerror("error", "please enter a valid integer")
    
    def delete_from_bst(self):
        # delete value from BST
        try:
            value = int(self.bst_input_entry.get())
            if self.bst.search(value):
                self.bst.delete(value)
                self.bst_input_entry.delete(0, tk.END)
                self.update_bst_display()
                messagebox.showinfo("success", f"value {value} deleted from BST")
            else:
                messagebox.showinfo("not found", f"value {value} not found in BST")
        except ValueError:
            messagebox.showerror("error", "please enter a valid integer")
    
    def search_bst(self):
        # search for value in BST
        try:
            value = int(self.bst_search_entry.get())
            node = self.bst.search(value)
            if node:
                messagebox.showinfo("search result", f"value {value} found in BST")
            else:
                messagebox.showinfo("search result", f"value {value} not found in BST")
        except ValueError:
            messagebox.showerror("error", "please enter a valid integer")
    
    def find_bst_min(self):
        # find minimum value in BST
        min_val = self.bst.minimum()
        if min_val is not None:
            messagebox.showinfo("minimum", f"minimum value: {min_val}")
        else:
            messagebox.showinfo("minimum", "BST is empty")
    
    def find_bst_max(self):
        # find maximum value in BST
        max_val = self.bst.maximum()
        if max_val is not None:
            messagebox.showinfo("maximum", f"maximum value: {max_val}")
        else:
            messagebox.showinfo("maximum", "BST is empty")
    
    def find_bst_predecessor(self):
        # find predecessor of value in BST
        try:
            value = int(self.bst_ps_entry.get())
            pred = self.bst.predecessor(value)
            if pred is not None:
                messagebox.showinfo("predecessor", f"predecessor of {value}: {pred}")
            else:
                messagebox.showinfo("predecessor", f"no predecessor found for {value}")
        except ValueError:
            messagebox.showerror("error", "please enter a valid integer")
    
    def find_bst_successor(self):
        # find successor of value in BST
        try:
            value = int(self.bst_ps_entry.get())
            succ = self.bst.successor(value)
            if succ is not None:
                messagebox.showinfo("successor", f"successor of {value}: {succ}")
            else:
                messagebox.showinfo("successor", f"no successor found for {value}")
        except ValueError:
            messagebox.showerror("error", "please enter a valid integer")
    
    def show_inorder(self):
        # show inorder traversal
        traversal = self.bst.inorder_traversal()
        if traversal:
            self.bst_display.delete(1.0, tk.END)
            self.bst_display.insert(tk.END, "Inorder traversal (sorted):\n")
            self.bst_display.insert(tk.END, " -> ".join(map(str, traversal)))
        else:
            messagebox.showinfo("empty", "BST is empty")
    
    def show_preorder(self):
        # show preorder traversal
        traversal = self.bst.preorder_traversal()
        if traversal:
            self.bst_display.delete(1.0, tk.END)
            self.bst_display.insert(tk.END, "Preorder traversal:\n")
            self.bst_display.insert(tk.END, " -> ".join(map(str, traversal)))
        else:
            messagebox.showinfo("empty", "BST is empty")
    
    def show_postorder(self):
        # show postorder traversal
        traversal = self.bst.postorder_traversal()
        if traversal:
            self.bst_display.delete(1.0, tk.END)
            self.bst_display.insert(tk.END, "Postorder traversal:\n")
            self.bst_display.insert(tk.END, " -> ".join(map(str, traversal)))
        else:
            messagebox.showinfo("empty", "BST is empty")
    
    def visualize_bst(self):
        # visualize BST structure
        visualization = self.bst.visualize_tree()
        self.bst_display.delete(1.0, tk.END)
        self.bst_display.insert(tk.END, "BST Structure:\n\n")
        self.bst_display.insert(tk.END, visualization)
    
    def update_bst_display(self):
        # update BST display with current contents
        self.bst_display.delete(1.0, tk.END)
        inorder = self.bst.inorder_traversal()
        if inorder:
            self.bst_display.insert(tk.END, "BST contents (inorder):\n")
            self.bst_display.insert(tk.END, " -> ".join(map(str, inorder)))
            self.bst_display.insert(tk.END, f"\n\nTotal nodes: {len(inorder)}")
        else:
            self.bst_display.insert(tk.END, "BST is empty")
    
    def create_hash_table_tab(self):
        # create hash table operations tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Hash Tables")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # hash table type selection
        type_frame = ttk.LabelFrame(main_frame, text="hash table type", padding=10)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.hash_table_type = tk.StringVar(value="Chaining")
        types = ["Chaining", "Linear Probing", "Double Hashing"]
        
        for ht_type in types:
            ttk.Radiobutton(type_frame, text=ht_type, variable=self.hash_table_type, value=ht_type).pack(anchor=tk.W)
        
        # operations frame
        ops_frame = ttk.LabelFrame(main_frame, text="operations", padding=10)
        ops_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # key-value input
        kv_frame = ttk.Frame(ops_frame)
        kv_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(kv_frame, text="key:").pack(side=tk.LEFT)
        self.key_entry = ttk.Entry(kv_frame, width=15)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(kv_frame, text="value:").pack(side=tk.LEFT)
        self.value_entry = ttk.Entry(kv_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)
        
        # operation buttons
        btn_frame = ttk.Frame(ops_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="insert", command=self.hash_insert).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="search", command=self.hash_search).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="delete", command=self.hash_delete).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="clear table", command=self.hash_clear).pack(side=tk.LEFT, padx=2)
        
        # performance testing
        perf_frame = ttk.LabelFrame(main_frame, text="performance testing", padding=10)
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(perf_frame, text="input sizes (comma separated):").pack(anchor=tk.W)
        self.ht_sizes_entry = ttk.Entry(perf_frame)
        self.ht_sizes_entry.pack(fill=tk.X, pady=2)
        self.ht_sizes_entry.insert(0, "10,100,1000,10000")
        
        ttk.Label(perf_frame, text="test runs per size:").pack(anchor=tk.W)
        self.ht_runs_entry = ttk.Entry(perf_frame)
        self.ht_runs_entry.pack(fill=tk.X, pady=2)
        self.ht_runs_entry.insert(0, "10")
        
        ttk.Button(perf_frame, text="run performance test", command=self.run_hash_performance_test).pack(pady=5)
        ttk.Button(perf_frame, text="Run Structure Comparison", command=self.run_structure_performance_test).pack(pady=5)
        # display frame
        display_frame = ttk.LabelFrame(main_frame, text="hash table contents", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.hash_display = tk.Text(display_frame)
        self.hash_display.pack(fill=tk.BOTH, expand=True)
        
        # initialize hash table
        self.hash_table = ChainingHashTable()
    
    def create_hash_table(self):
        # create a new hash table of selected type
        ht_type = self.hash_table_type.get()
        if ht_type == "Chaining":
            self.hash_table = ChainingHashTable()
        elif ht_type == "Linear Probing":
            self.hash_table = LinearProbingHashTable()
        elif ht_type == "Double Hashing":
            self.hash_table = DoubleHashingHashTable()
        self.update_hash_display()
    
    def hash_insert(self):
        # insert key-value pair into hash table
        try:
            key = self.key_entry.get()
            value = self.value_entry.get()
            if not key:
                messagebox.showerror("error", "key cannot be empty")
                return
            
            self.hash_table.insert(key, value)
            self.key_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
            self.update_hash_display()
        except Exception as e:
            messagebox.showerror("error", str(e))
    
    def hash_search(self):
        # search for key in hash table
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("error", "please enter a key to search")
            return
        
        value = self.hash_table.search(key)
        if value is not None:
            messagebox.showinfo("search result", f"key '{key}' found with value: {value}")
        else:
            messagebox.showinfo("search result", f"key '{key}' not found")
    
    def hash_delete(self):
        # delete key from hash table
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("error", "please enter a key to delete")
            return
        
        if self.hash_table.delete(key):
            messagebox.showinfo("success", f"key '{key}' deleted")
            self.update_hash_display()
        else:
            messagebox.showinfo("not found", f"key '{key}' not found")
    
    def hash_clear(self):
        # clear the current hash table
        self.create_hash_table()
        messagebox.showinfo("success", "hash table cleared")
    
    def update_hash_display(self):
        # update the hash table display
        self.hash_display.delete(1.0, tk.END)
        self.hash_display.insert(tk.END, f"Hash Table Type: {self.hash_table_type.get()}\n")
        self.hash_display.insert(tk.END, f"Size: {self.hash_table.size}\n")
        self.hash_display.insert(tk.END, f"Elements: {self.hash_table.count}\n")
        self.hash_display.insert(tk.END, f"Load Factor: {self.hash_table.load_factor():.2f}\n\n")
        
        if isinstance(self.hash_table, ChainingHashTable):
            self.hash_display.insert(tk.END, "Hash Table Contents:\n")
            for i, bucket in enumerate(self.hash_table.table):
                if bucket is not None:
                    self.hash_display.insert(tk.END, f"[{i}]: ")
                    current = bucket
                    while current is not None:
                        self.hash_display.insert(tk.END, f"{current.key}={current.value}")
                        if current.next is not None:
                            self.hash_display.insert(tk.END, " -> ")
                        current = current.next
                    self.hash_display.insert(tk.END, "\n")
        else:
            self.hash_display.insert(tk.END, "Hash Table Contents:\n")
            for i, node in enumerate(self.hash_table.table):
                if node is not None:
                    self.hash_display.insert(tk.END, f"[{i}]: {node.key}={node.value}\n")
    
    def run_hash_performance_test(self):
        # run performance comparison of hash table implementations
        try:
            sizes = [int(size.strip()) for size in self.ht_sizes_entry.get().split(",")]
            runs = int(self.ht_runs_entry.get())
        except ValueError:
            messagebox.showerror("error", "please enter valid sizes and runs")
            return
        
        # Test both successful and unsuccessful searches
        test_types = ["successful", "unsuccessful"]
        hash_types = ["Chaining", "Linear Probing", "Double Hashing"]
        
        results = {ht: {test: [] for test in test_types} for ht in hash_types}
        
        self.hash_display.delete(1.0, tk.END)
        self.hash_display.insert(tk.END, "running performance tests...\n")
        self.root.update()
        
        for size in sizes:
            self.hash_display.insert(tk.END, f"\ntesting size {size}:\n")
            
            # Generate test data
            test_data = [str(random.randint(1, size*10)) for _ in range(size)]
            search_data = test_data.copy()
            not_present_data = [str(random.randint(size*10 + 1, size*20)) for _ in range(size)]
            
            for ht_type in hash_types:
                # Create hash table
                if ht_type == "Chaining":
                    ht = ChainingHashTable(size*2)  # Larger size to keep load factor reasonable
                elif ht_type == "Linear Probing":
                    ht = LinearProbingHashTable(size*2)
                elif ht_type == "Double Hashing":
                    ht = DoubleHashingHashTable(size*2)
                
                # Insert all test data
                for key in test_data:
                    ht.insert(key, f"value_{key}")
                
                # Test successful searches
                start_time = time.time()
                for _ in range(runs):
                    for key in search_data[:100]:  # Limit to 100 searches per run
                        ht.search(key)
                successful_time = (time.time() - start_time) / runs
                results[ht_type]["successful"].append(successful_time)
                
                # Test unsuccessful searches
                start_time = time.time()
                for _ in range(runs):
                    for key in not_present_data[:100]:  # Limit to 100 searches per run
                        ht.search(key)
                unsuccessful_time = (time.time() - start_time) / runs
                results[ht_type]["unsuccessful"].append(unsuccessful_time)
                
                self.hash_display.insert(tk.END, 
                    f"{ht_type}: successful={successful_time:.6f}s, unsuccessful={unsuccessful_time:.6f}s\n")
                self.root.update()
        
        # Plot results
        self.figure.clear()
        
        # Successful searches plot
        ax1 = self.figure.add_subplot(121)
        for ht_type in hash_types:
            ax1.plot(sizes, results[ht_type]["successful"], label=ht_type, marker='o')
        ax1.set_xlabel('input size')
        ax1.set_ylabel('average time (seconds)')
        ax1.set_title('Successful Searches')
        ax1.legend()
        ax1.grid(True)
        if max(sizes) / min(sizes) > 100:
            ax1.set_xscale('log')
            ax1.set_yscale('log')
        
        # Unsuccessful searches plot
        ax2 = self.figure.add_subplot(122)
        for ht_type in hash_types:
            ax2.plot(sizes, results[ht_type]["unsuccessful"], label=ht_type, marker='o')
        ax2.set_xlabel('input size')
        ax2.set_ylabel('average time (seconds)')
        ax2.set_title('Unsuccessful Searches')
        ax2.legend()
        ax2.grid(True)
        if max(sizes) / min(sizes) > 100:
            ax2.set_xscale('log')
            ax2.set_yscale('log')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
    def run_structure_performance_test(self):
    # Run performance comparison of data structures
        try:
            sizes = [int(size.strip()) for size in self.ht_sizes_entry.get().split(",")]
            runs = int(self.ht_runs_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid sizes and runs")
            return
        
        structures = ["Array", "Linked List", "BST"]
        operations = ["Insertion", "Deletion", "Search"]
        
        # Initialize results dictionary
        results = {struct: {op: [] for op in operations} for struct in structures}
        
        self.hash_display.delete(1.0, tk.END)
        self.hash_display.insert(tk.END, "Running performance tests...\n")
        self.root.update()
        
        for size in sizes:
            self.hash_display.insert(tk.END, f"\nTesting size {size}:\n")
            
            # Test Array
            arr_times = {op: [] for op in operations}
            for _ in range(runs):
                test_data = [random.randint(1, size*10) for _ in range(size)]
                
                # Insertion (append)
                start = time.time()
                test_data.append(random.randint(1, size*10))
                arr_times["Insertion"].append(time.time() - start)
                
                # Deletion (remove last)
                start = time.time()
                if test_data:
                    test_data.pop()
                arr_times["Deletion"].append(time.time() - start)
                
                # Search
                target = random.choice(test_data) if test_data else 0
                start = time.time()
                target in test_data
                arr_times["Search"].append(time.time() - start)
            
            # Test Linked List
            ll_times = {op: [] for op in operations}
            for _ in range(runs):
                ll = LinkedList()
                for num in [random.randint(1, size*10) for _ in range(size)]:
                    ll.insert_at_head(num)
                
                # Insertion
                start = time.time()
                ll.insert_at_head(random.randint(1, size*10))
                ll_times["Insertion"].append(time.time() - start)
                
                # Deletion (remove head)
                start = time.time()
                if ll.head:
                    ll.head = ll.head.next
                    ll.size -= 1
                ll_times["Deletion"].append(time.time() - start)
                
                # Search
                lst = ll.to_list()
                target = random.choice(lst) if lst else 0
                start = time.time()
                ll.search(target)
                ll_times["Search"].append(time.time() - start)
            
            # Test BST
            bst_times = {op: [] for op in operations}
            for _ in range(runs):
                bst = BinarySearchTree()
                for num in [random.randint(1, size*10) for _ in range(size)]:
                    bst.insert(num)
                
                # Insertion
                start = time.time()
                bst.insert(random.randint(1, size*10))
                bst_times["Insertion"].append(time.time() - start)
                
                # Deletion
                lst = bst.inorder_traversal()
                target = random.choice(lst) if lst else 0
                start = time.time()
                bst.delete(target)
                bst_times["Deletion"].append(time.time() - start)
                
                # Search
                start = time.time()
                bst.search(target)
                bst_times["Search"].append(time.time() - start)
            
            # Calculate averages and store results
            for struct, times in zip(structures, [arr_times, ll_times, bst_times]):
                for op in operations:
                    avg_time = sum(times[op]) / runs * 1000  # Convert to milliseconds
                    results[struct][op].append(avg_time)
                    self.hash_display.insert(tk.END, 
                        f"{struct} {op}: {avg_time:.2f} ms\n")
                    self.root.update()
        
        # Plot results
        self.figure.clear()
        
        # Create one plot per operation
        for i, op in enumerate(operations):
            ax = self.figure.add_subplot(1, 3, i+1)
            for struct in structures:
                ax.plot(sizes, results[struct][op], label=struct, marker='o')
            ax.set_xlabel('Input Size')
            ax.set_ylabel('Time (ms)')
            ax.set_title(f'{op} Performance')
            ax.legend()
            ax.grid(True)
            if max(sizes) / min(sizes) > 100:
                ax.set_xscale('log')
        
        self.figure.tight_layout()
        self.canvas.draw()

class BinarySearchTree:
    # class implementing binary search tree functionality
    
    class Node:
        # nested class for BST nodes
        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None
    
    def __init__(self):
        # initialize empty BST
        self.root = None
        self.size = 0
    
    def insert(self, data):
        # insert data into BST
        self.root = self._insert_recursive(self.root, data)
        self.size += 1
    
    def _insert_recursive(self, node, data):
        # recursive helper for insertion
        if node is None:
            return self.Node(data)
        
        if data < node.data:
            node.left = self._insert_recursive(node.left, data)
        elif data > node.data:
            node.right = self._insert_recursive(node.right, data)
        # if data equals node.data, don't insert duplicate
        
        return node
    
    def delete(self, data):
        # delete data from BST
        self.root = self._delete_recursive(self.root, data)
    
    def _delete_recursive(self, node, data):
        # recursive helper for deletion
        if node is None:
            return node
        
        if data < node.data:
            node.left = self._delete_recursive(node.left, data)
        elif data > node.data:
            node.right = self._delete_recursive(node.right, data)
        else:
            # node to be deleted found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # node with two children - get inorder successor
            min_node = self._find_min_node(node.right)
            node.data = min_node.data
            node.right = self._delete_recursive(node.right, min_node.data)
            
        return node
    
    def search(self, data):
        # search for data in BST
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, node, data):
        # recursive helper for search
        if node is None or node.data == data:
            return node
        
        if data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)
    
    def minimum(self):
        # find minimum value in BST
        if self.root is None:
            return None
        return self._find_min_node(self.root).data
    
    def _find_min_node(self, node):
        # find node with minimum value
        while node.left is not None:
            node = node.left
        return node
    
    def maximum(self):
        # find maximum value in BST
        if self.root is None:
            return None
        node = self.root
        while node.right is not None:
            node = node.right
        return node.data
    
    def predecessor(self, data):
        # find predecessor of given value
        return self._predecessor_recursive(self.root, data, None)
    
    def _predecessor_recursive(self, node, data, predecessor):
        # recursive helper for predecessor
        if node is None:
            return predecessor
        
        if data <= node.data:
            return self._predecessor_recursive(node.left, data, predecessor)
        else:
            return self._predecessor_recursive(node.right, data, node.data)
    
    def successor(self, data):
        # find successor of given value
        return self._successor_recursive(self.root, data, None)
    
    def _successor_recursive(self, node, data, successor):
        # recursive helper for successor
        if node is None:
            return successor
        
        if data >= node.data:
            return self._successor_recursive(node.right, data, successor)
        else:
            return self._successor_recursive(node.left, data, node.data)
    
    def inorder_traversal(self):
        # return inorder traversal of BST (sorted order)
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        # recursive helper for inorder traversal
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self):
        # return preorder traversal of BST
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node, result):
        # recursive helper for preorder traversal
        if node is not None:
            result.append(node.data)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder_traversal(self):
        # return postorder traversal of BST
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node, result):
        # recursive helper for postorder traversal
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.data)
    
    def load_from_file(self, filename):
        # load BST data from file (one number per line)
        try:
            with open(filename, 'r') as file:
                for line in file:
                    self.insert(int(line.strip()))
            return True
        except Exception as e:
            print(f"error loading file: {e}")
            return False
    
    def visualize_tree(self):
        # create a visual representation of the tree
        if self.root is None:
            return "Tree is empty"
        
        lines = []
        self._visualize_recursive(self.root, lines, 0, "Root: ")
        return "\n".join(lines)
    
    def _visualize_recursive(self, node, lines, depth, prefix):
        # recursive helper for tree visualization
        if node is not None:
            lines.append("  " * depth + prefix + str(node.data))
            if node.left is not None or node.right is not None:
                if node.left is not None:
                    self._visualize_recursive(node.left, lines, depth + 1, "L--- ")
                else:
                    lines.append("  " * (depth + 1) + "L--- None")
                
                if node.right is not None:
                    self._visualize_recursive(node.right, lines, depth + 1, "R--- ")
                else:
                    lines.append("  " * (depth + 1) + "R--- None")

class HashTable:
    # Base class for hash table implementations
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None
    
    def __init__(self, size=101):
        self.size = size
        self.count = 0
    
    def hash_function1(self, key):
        return hash(key) % self.size
    
    def hash_function2(self, key):
        return 1 + (hash(key) % (self.size - 1))
    
    def insert(self, key, value):
        raise NotImplementedError
    
    def search(self, key):
        raise NotImplementedError
    
    def delete(self, key):
        raise NotImplementedError
    
    def load_factor(self):
        return self.count / self.size
    
    def resize(self, new_size):
        raise NotImplementedError


class ChainingHashTable(HashTable):
    # Hash table with chaining collision resolution
    def __init__(self, size=101):
        super().__init__(size)
        self.table = [None] * self.size
    
    def insert(self, key, value):
        index = self.hash_function1(key)
        if self.table[index] is None:
            self.table[index] = self.Node(key, value)
        else:
            current = self.table[index]
            while current.next is not None:
                if current.key == key:
                    current.value = value  # Update existing key
                    return
                current = current.next
            if current.key == key:
                current.value = value  # Update existing key
            else:
                current.next = self.Node(key, value)
        self.count += 1
    
    def search(self, key):
        index = self.hash_function1(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None
    
    def delete(self, key):
        index = self.hash_function1(key)
        current = self.table[index]
        prev = None
        while current is not None:
            if current.key == key:
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next
                self.count -= 1
                return True
            prev = current
            current = current.next
        return False


class LinearProbingHashTable(HashTable):
    # Hash table with linear probing collision resolution
    def __init__(self, size=101):
        super().__init__(size)
        self.table = [None] * self.size
    
    def insert(self, key, value):
        if self.load_factor() > 0.7:
            self.resize(self.size * 2)
        
        index = self.hash_function1(key)
        while self.table[index] is not None and self.table[index].key != key:
            index = (index + 1) % self.size
        
        if self.table[index] is None:
            self.count += 1
        self.table[index] = self.Node(key, value)
    
    def search(self, key):
        index = self.hash_function1(key)
        original_index = index
        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.size
            if index == original_index:
                break
        return None
    
    def delete(self, key):
        index = self.hash_function1(key)
        original_index = index
        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index] = None
                self.count -= 1
                self._rehash()
                return True
            index = (index + 1) % self.size
            if index == original_index:
                break
        return False
    
    def _rehash(self):
        old_table = self.table
        self.table = [None] * self.size
        self.count = 0
        for node in old_table:
            if node is not None:
                self.insert(node.key, node.value)
    
    def resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [None] * self.size
        self.count = 0
        for node in old_table:
            if node is not None:
                self.insert(node.key, node.value)


class DoubleHashingHashTable(HashTable):
    # Hash table with double hashing collision resolution
    def __init__(self, size=101):
        super().__init__(size)
        self.table = [None] * self.size
    
    def insert(self, key, value):
        if self.load_factor() > 0.7:
            self.resize(self.size * 2)
        
        index = self.hash_function1(key)
        step = self.hash_function2(key)
        attempts = 0
        
        while (self.table[index] is not None and 
               self.table[index].key != key and 
               attempts < self.size):
            index = (index + step) % self.size
            attempts += 1
        
        if attempts == self.size:
            raise Exception("Hash table is full")
        
        if self.table[index] is None:
            self.count += 1
        self.table[index] = self.Node(key, value)
    
    def search(self, key):
        index = self.hash_function1(key)
        step = self.hash_function2(key)
        original_index = index
        attempts = 0
        
        while (self.table[index] is not None and 
               attempts < self.size):
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + step) % self.size
            attempts += 1
            if index == original_index:
                break
        return None
    
    def delete(self, key):
        index = self.hash_function1(key)
        step = self.hash_function2(key)
        original_index = index
        attempts = 0
        
        while (self.table[index] is not None and 
               attempts < self.size):
            if self.table[index].key == key:
                self.table[index] = None
                self.count -= 1
                self._rehash()
                return True
            index = (index + step) % self.size
            attempts += 1
            if index == original_index:
                break
        return False
    
    def _rehash(self):
        old_table = self.table
        self.table = [None] * self.size
        self.count = 0
        for node in old_table:
            if node is not None:
                self.insert(node.key, node.value)
    
    def resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [None] * self.size
        self.count = 0
        for node in old_table:
            if node is not None:
                self.insert(node.key, node.value)   
        

# main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmPlatform(root)
    root.mainloop()