
from common import dummy, unittest, FlubberTestCase

import flubber
from flubber import locks


class LocksTests(FlubberTestCase):

    def test_semaphore(self):
        def func():
            lock = locks.Semaphore()
            lock.acquire()
            self.assertFalse(lock.acquire(blocking=False))
        flubber.spawn(func)
        self.loop.run()

    def test_bounded_semaphore(self):
        def func():
            lock = locks.BoundedSemaphore()
            lock.acquire()
            lock.release()
            self.assertRaises(ValueError, lock.release)
        flubber.spawn(func)
        self.loop.run()

    def test_rlock(self):
        lock = locks.RLock()
        def func1():
            lock.acquire()
            self.assertTrue(lock.acquire())
        def func2():
            self.assertFalse(lock.acquire(blocking=False))
        flubber.spawn(func1)
        flubber.spawn(func2)
        self.loop.run()

    def test_condition(self):
        d = dummy()
        d.value = 0
        cond = locks.Condition()
        def func1():
            with cond:
                self.assertEqual(d.value, 0)
                cond.wait()
                self.assertEqual(d.value, 42)
        def func2():
            with cond:
                d.value = 42
                cond.notify_all()
        flubber.spawn(func1)
        flubber.spawn(func2)
        self.loop.run()
