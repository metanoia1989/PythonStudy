#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from locust import LoadTestShape
from typing import Optional, Tuple

class MyCustomShape(LoadTestShape):
   time_limit = 600
   spawn_rate = 20
   
   def tick(self) -> Optional[Tuple[int, float]]:
       run_time = self.get_run_time()
       if run_time < self.time_limit:
           user_count = round(run_time, -2)
           return (user_count, self.spawn_rate)
       return None