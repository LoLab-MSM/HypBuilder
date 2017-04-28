
# A kernel density estimate based nested sampling method for computing evidence.
# New points are drawn from parameter space by first randomly selecting a point
# from the initial set, and then randomly selecting the new point from a
# multivariate normal distribution centered at the selected point. As the algorithm
# progresses an adaptive scalar reduces the variance and constricts the
# Gaussian kernels.

from math import *
import scipy
import numpy as np

class NS_KDE:

    def __init__(self, LH, data, prior):
        self.LH = LH
        self.data = data
        self.prior = prior
        self.iterations = 1000
        self.adaptive_scalar = 100.0
        self.scalar_limit = 1e-6
        self.Z = -1e300
        self.N = 10000
        self.working_set = []
        self._nested_sampling()

    def _initiate(self):

        # randomly sample from the parameter space to get an initial set of points
        for _ in range(self.N):
            point = []
            for each in self.prior:
                point.append(scipy.random.uniform(each[0], each[1]))
            self.working_set.append([self.LH(point), point])
        self.working_set.sort(reverse = True)

    def _nested_sampling(self):

        # initiate the run
        self._initiate()
        useless_samples = 0
        index = 1

        while index < self.iterations and self.adaptive_scalar > self.scalar_limit:

            # check number of non-viable samples taken from prior
            # shrink adaptive scalar, which shrinks the covariance matrix
            # when too many non-viable samples are taken from prior
            if useless_samples == 10:
                self.adaptive_scalar *= 0.99
                useless_samples = 0

            # sample from the prior using KDE
            test_point = self._KDE_sample()

            # check prior bounds
            bounded = True
            for i,each in enumerate(test_point):
                if each < self.prior[i][0] or each > self.prior[i][1]:
                    bounded = False

            if bounded:

                # calculate LH
                test_point_LH = self.LH(test_point)

                # check if sample is within likelihood bound
                if test_point_LH > self.working_set[-1][0]:

                    # update evidence and working set
                    LH_addition = self.working_set.pop()[0]
                    width = log(exp(-((float(index)-1) / self.N)) - exp(-(float(index) / self.N)))
                    self.Z = np.logaddexp(float(self.Z), (LH_addition + width))
                    self.working_set.append([test_point_LH, list(test_point)])
                    self.working_set.sort(reverse = True)
                    useless_samples = 0

                    index += 1

                else:
                    useless_samples += 1
            else:
                useless_samples += 1

        # add the likelihood from the working set
        for each in self.working_set:
            increment = (each[0] - log(self.N) + log(exp(-(float(index)/self.N))))
            self.Z = np.logaddexp(float(self.Z), increment)

        # compute the mean of the data
        sum_data = 0
        for each in self.working_set:
            sum_data += each[0]
        mean = sum_data / len(self.working_set)

        # compute the variance of the data
        # small likelihood variance -> algorithm termination
        sum_squared_diff = 0
        for each in self.working_set:
            sum_squared_diff += (each[0] - mean) ** 2
        self.variance = sum_squared_diff / (len(self.working_set) - 1)

        return self.Z

    def _KDE_sample(self):

        # # construct covariance matrix
        # param_obs = []
        # for each in self.working_set:
        #     param_obs.append(each[1])
        # param_obs_T = np.array(param_obs).T
        # cov = self.adaptive_scalar*np.cov(param_obs_T)
        #
        # # crude correction to the covariance matrix
        # # np.cov() can result in small negative eigenvalues, likely due to rounding error
        # cov = np.identity(len(cov))*np.diag(cov)

        # construct simplistic covariance matrix
        cov = self.adaptive_scalar*np.identity(len(self.prior))

        # select data point
        data_point = np.random.randint(0, len(self.working_set))
        coordinates = self.working_set[data_point][1]

        # select prior point from kernel around data point
        new_point = np.random.multivariate_normal(coordinates, cov)

        return new_point

print



