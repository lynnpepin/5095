import unittest as ut
import numpy as np

from toolkit import Node, Swarm, polar_to_xy

from palette import S16, s16_raw, interpolate_color

class NodeTests(ut.TestCase):
    def test_updated_hist(self):
        for _ in range(10):
            x, y = np.random.uniform(-100, 100, 2)
            hist_length = np.random.randint(1,10)
            some_node = Node(x=x, y=y, hist_length=hist_length)
            for _ in range(100):
                x, y = np.random.uniform(-100, 100, 2)
                some_node.update(x=x, y=y)

                # check new value is indeed there...
                self.assertEqual(some_node.X[0], x)
                self.assertEqual(some_node.Y[0], y)
                # ... and length
                self.assertEqual(len(some_node.X), hist_length)
                self.assertEqual(len(some_node.Y), hist_length)

    def test_hist_update(self):
        for _ in range(10):
            length = 20
            # update 20 times, and make sure Xs and Ys correspond
            x, y = np.random.uniform(-100, 100, 2)
            some_node = Node(x=x, y=y, hist_length=length)

            xs = list(np.random.uniform(-100, 100, length))
            ys = list(np.random.uniform(-100, 100, length))

            # Do 20 updates!
            for ii in range(length):
                some_node.update(x = xs[ii], y = ys[ii])

            # These should be equal!
            # [::-1] is shorthand for 'reversed'
            self.assertEqual(some_node.X[:length], xs[::-1])
            self.assertEqual(some_node.Y[:length], ys[::-1])

class SwarmTests(ut.TestCase):
    def test_swarm_lengths(self):
        for _ in range(100):
            num_nodes = np.random.randint(1,40)
            hist_length = np.random.randint(1,40)
            swarm = Swarm(N=num_nodes, hist_length=hist_length)

            # Test number of nodes and hist_length
            self.assertEqual(len(swarm.nodes), num_nodes)
            for node in swarm.nodes:
                self.assertEqual(len(node.X), hist_length)
                self.assertEqual(len(node.Y), hist_length)

class UtilTests(ut.TestCase):
    def test_polar_to_xy(self):
        for _ in range(100):
            theta = np.random.uniform(-200, 200)
            r = np.random.uniform(-100, 100)
            x = np.cos(theta)*r
            y = np.sin(theta)*r
            computed_xy = polar_to_xy(r, theta)
            self.assertAlmostEqual(computed_xy, (x,y))
    
    def test_polar_to_xy_edgecases(self):
        self.assertEqual(
            polar_to_xy(0, 0),
            (0,0)
        )
        self.assertEqual(
            polar_to_xy(0, 1000000000000000000),
            (0,0)
        )

class PaletteTests(ut.TestCase):
    def test_sanity_s16_raw(self):
        self.assertEqual(s16_raw.shape, (16, 3))
    
    def test_sanity_s16(self):
        this_should_work = S16.lime + S16.navy
    
    def test_sanity_interpolate(self):
        for color1 in s16_raw:
            for color2 in s16_raw:
                np.testing.assert_equal(
                    color1,
                    interpolate_color(color1, color2, r=0)
                )
                np.testing.assert_equal(
                    color2,
                    interpolate_color(color1, color2, r=1)
                )



if __name__ == '__main__':
    # Run the tests
    ut.main(verbosity=2)