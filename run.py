import os, sys
from optparse import OptionParser
from lib import master, functions

pr = OptionParser(usage="%prog model [options]")
pr.add_option("-q"  , "--queue"         , dest="queue"       , type="string"      , default=None , help="Queue name to run on the batch system.")
pr.add_option("-i"  , "--input"         , dest="inputdir"    , type="string"      , default=None , help="Input directory to read datacards from")
pr.add_option("--pdir"                  , dest="publdir"     , type="string"      , default=None , help="Publication dir to copy the final plot to")
pr.add_option("--pname"                 , dest="publname"    , type="string"      , default=None , help="Publication name to rename/copy the final plot")
pr.add_option("--fp"                    , dest="poolonly"    , action="store_true", default=False, help="Only consider what is inside the pool, do NOT consider any input directory")
pr.add_option("--fi"                    , dest="indironly"   , action="store_true", default=False, help="Only consider what is inside the input directory, do NOT consider the pool")
pr.add_option("-F"                      , dest="forceImport" , action="store_true", default=False, help="Reimport packages from the input directory if they already exist in the pool.")
pr.add_option("-l"  , "--lumis"         , dest="lumis"       , action="append"    , default=[]   , help="Luminosities in the input directory to consider")
pr.add_option("-r"  , "--regions"       , dest="regions"     , action="append"    , default=[]   , help="Regions in the input directory to consider")
pr.add_option("-p"  , "--packages"      , dest="packages"    , action="append"    , default=[]   , help="Packages to combineelamente")
pr.add_option("--ca", "--combineAll"    , dest="cmbAll"      , action="store_true", default=False, help="All selected packages will be combined")
pr.add_option("--cl", "--combineLumis"  , dest="cmbLumis"    , action="append"    , default=[]   , help="Combine these luminosities if they have common regions.")
pr.add_option("--cr", "--combineRegions", dest="cmbRegions"  , action="append"    , default=[]   , help="Combine these regions if they are present in the same luminosity.")
pr.add_option("--ap", "--addPackages"   , dest="addPackages" , action="append"    , default=[]   , help="Packages to add to all the others, which are run separately.")
pr.add_option("-X", "--excludeTiers"    , dest="excludeTiers", action="append"    , default=[]   , help="Tiers to exclude")
pr.add_option("-R", "--redoTiers"       , dest="redoTiers"   , action="append"    , default=[]   , help="Tiers to redo")
pr.add_option("-S", "--stopAtTier"      , dest="stopAtTier"  , type="string"      , default=None , help="Stop execution after running this tier")
pr.add_option("-M", "--mode"            , dest="mode"        , type="string"      , default=None , help="Give the name of the plot mode that you want to use, i.e. 'xsec' for 0.95 CL upper limit on cross section (default), 'sens' for sensitivity, 'braz' for brazilian flag plot (not yet implemented). Default is the value of the module, else use 'xsec'")
pr.add_option("--qall"                  , dest="qall"        , action="store_true", default=False, help="Run EVERYTHING on the batch system (also summary, histo, smear and plot tier)")
pr.add_option("--ext"                   , dest="plotExt"     , type="string"      , default="C,png,pdf,root", help="File extensions to save the final plot in (default: pdf, root, C)")
pr.add_option("-e", "--energy"          , dest="energy"      , type="string"      , default="13"        , help="Center-of-mass energy in TeV")
pr.add_option("--preliminary"           , dest="preliminary" , type="string"      , default="Preliminary", help="Additional text to be plotted next to CMS (e.g. Preliminary, Internal)")
pr.add_option("--inspect"               , dest="inspect"     , action="store_true", default=False, help="Inspect intermediate results before going to the next tier")
pr.add_option("--view"                  , dest="view"        , action="store_true", default=False, help="View what is currently in the pool and bundle repository (AFTER any possible import is done)")
pr.add_option("-v"                      , dest="verbosity"   , type="int"         , default=1    , help="Verbosity level (0 = nothing, 1 = tiers and jobcontrol, 2 = everything, 3 = debugging [not yet implemented])")
pr.add_option("-b", "--bundle"          , dest="bundle"      , type="string"      , default=0    , help="Name of the bundle to use")
pr.add_option("--remark"                , dest="remark"      , type="string"      , default=0    , help="Add a remark to that bundle (something like 'new configuration' or 'test' or whatnot)")
pr.add_option("--m2"                    , dest="mass2"       , type="float"       , default=0    , help="Give the mass of the second particle in order to be able to run plotmode 'braz' in case of many second masses")
pr.add_option("--yrange"                , dest="rangeY"      , type="string"      , default=None , help="Bypass rangeY in env/models")
pr.add_option("--zrange"                , dest="rangeZ"      , type="string"      , default=None , help="Bypass rangeZ in env/models")
pr.add_option("--points"                , dest="points"      , action="append"    , default=[]   , help="Points to consider")
pr.add_option("--toys"                  , dest="toys"        , action="store_true", default=False, help="Evaluate limits using toys")

(options, args) = pr.parse_args()

theDir = os.path.dirname(os.path.realpath(sys.argv[0]))
if not os.path.exists(theDir+"/init"):
    functions.cmd(None, "touch "+theDir+"/init")

SPM = master.SPM(args, options)





