IOP = [96.8, 111.6, 125, 142.8, 160.8, 178.6, 201, 223.4, 250.4, 314.8, 366, 416.4, 466.8, 518, 619.6, 700, 800, 900,
       1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500]

def find_velocity_by_formula(discharge, id_of_pipe):
    velocity = discharge * (4 / (3.14 * (id_of_pipe / 1000) ** 2))
    return round(velocity, 5)



class Pipe:
    def __init__(self,index, start_node, end_node, length, discharge,
                 ground_level_start, ground_level_end, rhas, manual_iop, min_vel=0.6, max_vel=3,
                 iop_list=None, parent_pipe_index=None):
        if iop_list is None:
            iop_list = IOP
        self.iop_list = iop_list
        self.min_vel = min_vel
        self.max_vel = max_vel
        self.index = index
        self.start_node = start_node
        self.end_node = end_node
        self.length = float(length)
        self.discharge = float(discharge)
        self.ground_level_start = float(ground_level_start)
        self.ground_level_end = float(ground_level_end)
        self.is_village_endpoint = "V" in self.end_node
        self.allowed_iops = self.find_allowed_iops()
        self.manual_iop = manual_iop
        self.iop = self.allowed_iops[0] if self.manual_iop is None else self.manual_iop
        self.parent_iop = self.iop_list[-1]
        self.parent_pipe_index = parent_pipe_index
        self.velocity = self.find_velocity()
        self.rhas = rhas
        self.diff_in_g_level = self.ground_level_start - self.ground_level_end
        self.fhl = self.find_fhl()
        self.rhae = self.find_rhae()




    def find_velocity(self):
        velocity = self.discharge * (4 / (3.14 * (self.iop / 1000) ** 2))
        return float(round(velocity, 2))

    def find_fhl(self, cr_value=1):
        fhl = ((self.length * (self.discharge / cr_value) ** 1.81) / (994.62 * (self.iop / 1000) ** 4.81)) * 1.1
        return float(round(fhl, 2))

    def find_rhae(self):
        rhae = (self.diff_in_g_level + self.rhas) - self.fhl
        return float(round(rhae, 2))

    def find_allowed_iops(self):
        allowed_iops = []
        for iop in self.iop_list:
            vel = find_velocity_by_formula(discharge=self.discharge, id_of_pipe=iop)
            if self.max_vel >= vel >= self.min_vel:
                allowed_iops.append(iop)
        if not allowed_iops:
            allowed_iops = self.iop_list
        return allowed_iops