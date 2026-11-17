import time


class VM:
    def __init__(self, vm_id, speed=1.0):
        self.vm_id = vm_id
        self.speed = speed
        self.available_at = 0.0


class CloudSimulation:
    def __init__(self):
        self.clock = 0.0
        self.paused = False
        self.vms = [VM("VM-1"), VM("VM-2")]
        self.jobs = [
            {"id": "J1", "duration": 3},
            {"id": "J2", "duration": 4},
            {"id": "J3", "duration": 2},
            {"id": "J4", "duration": 5},
            {"id": "J5", "duration": 2},
        ]
        self.events = []

    def pause(self):
        self.paused = True
        print(f"\n[CONTROL] Simulation paused at t={self.clock}")

    def resume(self):
        self.paused = False
        print(f"[CONTROL] Simulation resumed at t={self.clock}")

    def add_vm(self, vm_id, speed=1.0):
        self.vms.append(VM(vm_id, speed))
        print(f"[ENTITY] Dynamically created {vm_id} (speed={speed})")

    def run_until(self, stop_time):
        while self.clock < stop_time:
            if self.paused:
                print("Simulation is paused.")
                return
            self.clock += 1
            self.schedule_ready_jobs()
            time.sleep(0.15)

    def schedule_ready_jobs(self):
        while self.jobs:
            vm = min(self.vms, key=lambda item: item.available_at)
            if vm.available_at > self.clock:
                break
            job = self.jobs.pop(0)
            start = max(self.clock, vm.available_at)
            finish = start + job["duration"] / vm.speed
            vm.available_at = finish
            self.events.append((job["id"], vm.vm_id, round(start, 2), round(finish, 2)))
            print(f'  {job["id"]} -> {vm.vm_id}: start={start:.1f}, finish={finish:.1f}')

    def run_to_completion(self):
        while self.jobs:
            if self.paused:
                return
            self.clock += 1
            self.schedule_ready_jobs()
            time.sleep(0.15)
        self.clock = max([self.clock] + [vm.available_at for vm in self.vms])


if __name__ == "__main__":
    sim = CloudSimulation()
    sim.run_until(5)
    sim.pause()
    sim.add_vm("VM-3", speed=1.5)
    sim.resume()
    sim.run_to_completion()

    print("\nFinal VM entities:")
    for vm in sim.vms:
        print(f"  {vm.vm_id} available at {round(vm.available_at, 2)}")

    print("\nEvent log:")
    for event in sim.events:
        print(event)