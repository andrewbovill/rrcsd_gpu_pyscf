import time
from pyscf import gto, scf, cc
from rccsd_gpu import RCCSD_GPU

# Pentane
atom = """C  -1.05510   -0.65800    0.24460
    C  -0.97160    0.78050   -0.23490
    C   0.29520   -1.23270   -0.15360
    C   0.44690    1.19150    0.13090
    C   1.28460   -0.08140    0.01300
    H  -1.17420   -0.68960    1.33400
    H  -1.88870   -1.20200   -0.20820
    H  -1.10920    0.82650   -1.32170
    H  -1.72400    1.42200    0.23270
    H   0.56830   -2.10410    0.44890
    H   0.27130   -1.54810   -1.20360
    H   0.82100    1.99340   -0.51270
    H   0.47590    1.55600    1.16480
    H   1.89790   -0.21640    0.91060
    H   1.96550   -0.03230   -0.84350"""

caffeine = """O 0.4700    2.5688    0.0006 
    O -3.1271   -0.4436   -0.0003 
    N -0.9686   -1.3125    0.0000 
    N 2.2182    0.1412   -0.0003 
    N -1.3477    1.0797   -0.0001 
    N 1.4119   -1.9372    0.0002 
    C 0.8579    0.2592   -0.0008 
    C 0.3897   -1.0264   -0.0004 
    C 0.0307    1.4220   -0.0006 
    C -1.9061   -0.2495   -0.0004 
    C 2.5032   -1.1998    0.0003 
    C -1.4276   -2.6960    0.0008 
    C 3.1926    1.2061    0.0003 
    C -2.2969    2.1881    0.0007 
    H 3.5163   -1.5787    0.0008 
    H -1.0451   -3.1973   -0.8937 
    H -2.5186   -2.7596    0.0011 
    H -1.0447   -3.1963    0.8957 
    H 4.1992    0.7801    0.0002 
    H 3.0468    1.8092   -0.8992 
    H 3.0466    1.8083    0.9004 
    H -1.8087    3.1651   -0.0003 
    H -2.9322    2.1027    0.8881 
    H -2.9346    2.1021   -0.8849 """

mol = gto.M(atom=caffeine, basis="sto3g", verbose=4, max_memory=50000)
mf = scf.RHF(mol).run()

_t1 = time.time()
my_cc1 = cc.rccsd.RCCSD(mf)
my_cc1.max_cycle = 1
my_cc1.kernel()
print(f"CPU RCCSD time = {time.time()-_t1:.2e} (s)")

_t2 = time.time()
my_cc2 = RCCSD_GPU(mf)
my_cc2.max_cycle = 1
my_cc2.kernel()
print(f"GPU RCCSD time = {time.time()-_t2:.2e} (s)")

