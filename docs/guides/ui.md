# UI 模块

> 模块： `borax.ui`

## aiotk：异步支持

使用方法：

```python
import tkinter as tk
import asyncio

from borax.ui.aiotk import run_loop

class App(tk.Tk):
  def __init__(self):
        super().__init__()
        self.title('Async Demo')

app = App()
loop = asyncio.get_event_loop()
loop.run_until_complete(run_loop(app))
```