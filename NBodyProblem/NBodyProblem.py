"""Simulation of N-body-Problem."""
#
# Karsten Benz (C) 2023
#

from math import sqrt
import pprint as pp


class NBodyProblem:
    """N-Body-Problem Solver Classs."""

    def __init__(self, g=6.6743e-11, trail=100):

        self.N = 0
        self.G = g  # [ m^3 * kg^-1 * s^-1 ]
        self.dt = 1 # delta time
        self.trail = trail # number of positions for a trail

        self.pos = []
        self.vel = []
        self.mass = []
        self.name = []
        self.enabled = []
        self.sizes = [2]  # size of initial marker

    def add_body(self, name, enabled, mass, x, y, z, vx, vy, vz):
        """Add new body."""

        self.name.append(name)
        self.mass.append(mass)
        self.enabled.append(enabled)

        self.pos.append([])
        self.pos[self.N] = []
        self.pos[self.N].append([x, y, z])

        self.vel.append([])
        self.vel[self.N] = [vx, vy, vz]

        self.N += 1

        return self.N - 1

    def set_body(self, name, enabled, mass, x, y, z, vx, vy, vz):

        # find index
        try:
            idx = self.name.index(name)
        except:
            idx = -1

        if idx == -1:
            self.add_body(name, enabled, mass, x, y, z, vx, vy, vz)
        else:
            self.name[idx] = name
            self.mass[idx] = mass
            self.enabled[idx] = enabled

            self.pos[idx] = []
            self.pos[idx].append([x, y, z])

            self.vel[idx] = [vx, vy, vz]

    def iterate(self):

        
        for j in range(self.N):

            # skip disabled bodies
            if not self.enabled[ j ]:
                continue

            disp_vec = [0.0, 0.0, 0.0]
            acc      = [0.0, 0.0, 0.0]

            for i in range(self.N):
                # skip itself or disabled bodies
                if i == j or not self.enabled[ j ]:
                    continue

                for k in range(3):
                    disp_vec[k] = self.pos[i][-1][k] - self.pos[j][-1][k]

                disp_len = sqrt(disp_vec[0] ** 2 + disp_vec[1] ** 2 + disp_vec[2] ** 2)


                #  a = F / m
                #
                #  Fv = G*m*M * dv / |dv|^3
                #  
                #  dv: displacement vector
                #
                gmmd = self.G * self.mass[i] / disp_len ** 3

                for k in range(3):
                    acc[k] += gmmd * disp_vec[ k ]

                # print("{}->{}: dist={} acc={} vec={}".format(self.name[j], self.name[i], disp_len, acc, disp_vec))

            # Set new speed
            for k in range(3):
                self.vel[j][k] += acc[k]

        for j in range(self.N):

            new_pos = [0.0, 0.0, 0.0]

            # skip disabled bodies
            if not self.enabled[ j ]:
                continue

            # Append new position
            for k in range(3):
                new_pos[k] = self.pos[j][-1][k] + self.vel[j][k] * self.dt
            self.pos[j].append(new_pos)

            # pop beginning of trail
            if (len(self.pos[j]) > self.trail):
                self.pos[j].pop(0)

    def dump_bodies(self):
        for i in range(len(self.name)):
            print(self.name[i], self.enabled[i], self.mass[i], self.pos[i], self.vel[i])

    def print_pos(self):
        print('\n\nPosition Matrix:\n')
        for i in range(len(self.name)):
            print("\n{}\n".format(self.name[i]))
            pp.pprint(self.pos[i])
