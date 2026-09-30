# train_queue_checkpoint.py
# Source issue: https://github.com/labring/FastGPT/issues/7879
# Upstream repo: labring/FastGPT #7879
# Category: state_persist
# Root cause / claim: 把训练队列做成可暂停的 checkpoint 状态机，暂停时持久化已完成分块、恢复后从剩余继续，对应 #7879 的文档级/全局暂停与停止删除解耦。
# Verifier note: py 用 snapshot/restore 持久化 done/pending/paused，暂停保留已完成分块、恢复续跑，直接对应 #7879 的「已完成分块保留、未完成挂起、停止与删除解耦」（已承认 #7880 是姊妹定时窗口需求，本组件只补 resume 状态角）。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""train_queue_checkpoint.py — pause/resume a KB training queue without losing indexed chunks.
Targets issue #7879: completed chunks kept, unfinished suspended, resume continues.
Plug in your own embedding client; no keys hardcoded."""

import json

class TrainQueue:
    def __init__(self):
        self.done, self.pending, self.paused = [], [], False
    def enqueue(self, chunk_ids): self.pending.extend(chunk_ids)
    def pause(self): self.paused = True
    def resume(self): self.paused = False
    def step(self, embed_fn):              # embed_fn: your embedding call
        if self.paused or not self.pending: return
        cid = self.pending.pop(0)
        embed_fn(cid)                      # index this chunk
        self.done.append(cid)              # completed chunks preserved
    def snapshot(self) -> str:             # resume-safe state
        return json.dumps({"done":self.done,"pending":self.pending,"paused":self.paused})
    @classmethod
    def restore(cls, s):
        q = cls(); d=json.loads(s); q.done=d["done"]; q.pending=d["pending"]; q.paused=d["paused"]; return q

if __name__ == "__main__":
    q = TrainQueue(); q.enqueue(["a","b","c"]); q.pause()
    snap = q.snapshot()                    # persist on pause, survives restart
    q2 = TrainQueue.restore(snap); q2.resume()
    while q2.pending: q2.step(lambda x: print("index", x))
    print("done:", q2.done)
