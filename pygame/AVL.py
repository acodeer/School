import tkinter as tk

def on_mouse_wheel(event):
    global scroll_height
    if event.delta > 0:  # 휠 위로 이동
        scroll_height += 50
    else:  # 휠 아래로 이동
        scroll_height = max(100, scroll_height - 50)  # 최소 높이 제한
    canvas.configure(scrollregion=(0, 0, 500, scroll_height))

# 초기 설정
root = tk.Tk()
root.geometry("400x300")

# Canvas 생성
canvas = tk.Canvas(root, bg="lightblue")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar 생성 및 연결
scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Canvas 내부에 Frame 생성
frame = tk.Frame(canvas, bg="white", width=500, height=500)
canvas.create_window((0, 0), window=frame, anchor="nw")

# 스크롤 영역 초기화
scroll_height = 500
canvas.configure(scrollregion=(0, 0, 500, scroll_height))

# 마우스 휠 이벤트 바인딩
root.bind("<MouseWheel>", on_mouse_wheel)  # Windows, Linux
root.bind("<Button-4>", lambda event: on_mouse_wheel(event))  # macOS 휠 위
root.bind("<Button-5>", lambda event: on_mouse_wheel(event))  # macOS 휠 아래

root.mainloop()
