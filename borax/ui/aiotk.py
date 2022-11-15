import tkinter as tk
import asyncio

__all__ = ['run_loop']


async def run_loop(app, interval=0.05):
    try:
        while True:
            app.update()
            await asyncio.sleep(interval)
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise
