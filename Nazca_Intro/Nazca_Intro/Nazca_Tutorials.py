# Implement the Nazca tutorials: https://nazca-design.org/tutorials/

import sys # access system routines

# Have to tell Visual Studio where the Nazca package is located to ensure it works
sys.path.append('c:/program files (x86)/microsoft visual studio/shared/anaconda3_64/lib/site-packages/')
import nazca
import nazca.demofab as demo

MOD_NAME_STR = "Nazca_Tutorials"

def Example_1():
    # run this example to make sure everything is working correctly
    # https://nazca-design.org/manual/

    FUNC_NAME = ".Example_1()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # draw some waveguides and write them to the generic gds file
        nazca.strt(length=20).put()
        nazca.bend(angle=90).put()
        nazca.bend(angle=-180).put()
        nazca.strt(length=10).put()

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def Example_2():
    # run this example to make sure everything is working correctly
    # https://nazca-design.org/manual/

    FUNC_NAME = ".Example_2()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # draw some waveguides at absolute positions and write them to the generic file
        nazca.strt(length=5).put(0)
        nazca.strt(length=10, width=4).put(0,10)
        nazca.bend(angle=90, radius=10).put(15,10,-90)

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def Example_3():
    # run this example to make sure everything is working correctly
    # In this example we additionally import the demonstration foundry “demofab” that comes with Nazca. Demofab has predefined 
    # building blocks and interconnects that are technology compliant with a virtual technology. It is for playing around and gets 
    # you ready for designing in Nazca in any technology, because the exact same concepts apply to any PDK in Nazca, like Silicon 
    # Photonics, InP, SiN, glass and polymers PDKs.

    # This example creates a 1x2 MMI and connects waveguides using chain connections. Interconnects have been predefined in the PDK 
    # and we use the demo.shallow waveguide.

    # By assigning name mmi1 to the MMI, we can refer to any of mmi1 its ports (‘a0’, ‘b0’, ‘b1’) via the Python dictionary mmi1.pin. 
    # This comes in very useful when building a circuit:
    # https://nazca-design.org/manual/

    FUNC_NAME = ".Example_3()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # use the nazca demofab to draw a device
        mmi1 = demo.mmi1x2_sh().put()
        demo.shallow.strt(length=50).put(mmi1.pin['a0'])
        demo.shallow.sbend(offset=20).put(mmi1.pin['b0'])
        demo.shallow.sbend(offset=-20).put(mmi1.pin['b1'])

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def Example_4():
    # https://nazca-design.org/crate-bb-using-polygon/
    # In Nazca it is very simple to create new building blocks and build hierarchical designs. The hierarchy in Nazca can 
    # be directly transferred to the exported GDS file. Nazca calls a building block a ‘Cell’ object, because it will be 
    # exported as a cell in GDS.

    # This example creates a building block from a 1x2 MMI and three in-out waveguides. Next, the new block is put several times in the mask.

    FUNC_NAME = ".Example_4()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # create a layer and define its accuracy       

        with nazca.Cell(name='myMMI') as mmi:
            mmi1 = demo.mmi1x2_sh().put()
            demo.shallow.strt(length=50).put(mmi1.pin['a0'])
            demo.shallow.sbend(offset=20).put(mmi1.pin['b0'])
            demo.shallow.sbend(offset=-20).put(mmi1.pin['b1'])

        mmi.put(0)
        mmi.put(0, 100)
        mmi.put(300, 50)

        nazca.export_gds()

        pass
    except Exception:
        print(ERR_STATEMENT)

def Example_5():
    # https://nazca-design.org/crate-bb-using-polygon/
    # A building block needs pins to connect it to the rest of a layout, e.g. interconnects or other building blocks. 
    # Note that in the Nazca philosophy of chain connections, the pins always point outwards from a building block; 
    # This avoids a lot of confusion and trial and error when building a circuit. If pins are not explicitly defined 
    # in a cell, then pins ‘a0’ and ‘b0’ are automatically added at the cell origin, with ‘a0’ pointing in the negative x, 
    # i.e. (0, 0, 180) and ‘b0’ in the positive x-direction, i.e. (0, 0, 0). By default, a building block is placed with 
    # its ‘a0’ port at the indicated position in the put method. To choose another port you can simple place the name of 
    # the pin to place the block as first argument in put, e.g. put(‘b0’) to place port ‘b0’ at (0, 0 , 0) or 
    # put(‘b0’, 0, 100, 90) to place port ‘b0’ at (0, 100, 90).
    
    FUNC_NAME = ".Example_5()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        with nazca.Cell(name='myMMI') as mmi:
            mmi1 = demo.mmi1x2_sh().put()
            elm1 = demo.shallow.strt(length=50).put(mmi1.pin['a0'])
            elm2 = demo.shallow.sbend(offset=20).put(mmi1.pin['b0'])
            elm3 = demo.shallow.sbend(offset=-20).put(mmi1.pin['b1'])

            nazca.Pin('a0', pin = elm1.pin['b0']).put()
            nazca.Pin('b0', pin = elm2.pin['b0']).put()
            nazca.Pin('b1', pin = elm3.pin['b0']).put()

        mmi.put('a0',0) # same as mmi.put(0), 'a0' is the default
        mmi.put('b0', 0, 100)

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def mmi(offset = 40, name = 'mmi'):
    with nazca.Cell(name = name) as mmi:
        mmi1 = demo.mmi1x2_sh().put()

        elm1 = demo.shallow.strt(length=50).put(mmi1.pin['a0'])
        elm2 = demo.shallow.sbend(offset=offset).put(mmi1.pin['b0'])
        elm3 = demo.shallow.sbend(offset=-offset).put(mmi1.pin['b1'])

        nazca.Pin('a0', pin = elm1.pin['b0']).put() # Input Pin definition
        nazca.Pin('b0', pin = elm2.pin['b0']).put() # Output Pin one
        nazca.Pin('b1', pin = elm3.pin['b0']).put() # Output Pin two

    return mmi

def Example_6():
    # Example 6
    # In this example a parametrized MMI building block is constructed by placing a Cell definition inside a Python 
    # function definition. We use the building block containing the MMI with in-out waveguides of the previous example 
    # and parametrize the output pitch. Doing so provides a nice way to draw a 1x8 splitter. Additionally, a straight guide 
    # of the demo.shallow interconnect type is connected to one of the 1x8 splitter outputs.

    FUNC_NAME = ".Example_6()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        mmi1 = mmi(offset = 100, name = 'mmi1').put(0)

        mmi2a = mmi(offset = 50, name = 'mmi2').put(mmi1.pin['b0'])
        mmi2b = mmi(offset = 50, name = 'mmi3').put(mmi1.pin['b1'])

        mmi3a = mmi(offset = 25, name = 'mmi4').put(mmi2a.pin['b0'])
        mmi3b = mmi(offset = 25, name = 'mmi5').put(mmi2a.pin['b1'])

        mmi3c = mmi(offset = 25, name = 'mmi6').put(mmi2b.pin['b0'])
        mmi3d = mmi(offset = 25, name = 'mmi7').put(mmi2b.pin['b1'])

        #demo.shallow.strt(length = 200).put(mmi3c.pin['b0'])

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def splitter_1by8(name = 'splitter'):
    # can use the code from the last example to make a splitter
    # this can be put in its own module, called, splitter for example
    # sample call: split = splitter_1by8().put(0)

    with nazca.Cell(name = name) as splitter_1x8:
        mmi1 = mmi(offset = 100, name = 'mmi1').put(0)

        mmi2a = mmi(offset = 50, name = 'mmi2').put(mmi1.pin['b0'])
        mmi2b = mmi(offset = 50, name = 'mmi3').put(mmi1.pin['b1'])

        mmi3a = mmi(offset = 25, name = 'mmi4').put(mmi2a.pin['b0'])
        mmi3b = mmi(offset = 25, name = 'mmi5').put(mmi2a.pin['b1'])

        mmi3c = mmi(offset = 25, name = 'mmi6').put(mmi2b.pin['b0'])
        mmi3d = mmi(offset = 25, name = 'mmi7').put(mmi2b.pin['b1'])

        nazca.Pin('a0', pin=mmi1.pin['a0']).put() # Input Pin definition
        nazca.Pin('b0', pin=mmi3a.pin['b0']).put()
        nazca.Pin('b1', pin=mmi3a.pin['b1']).put()
        nazca.Pin('b2', pin=mmi3b.pin['b0']).put()
        nazca.Pin('b3', pin=mmi3b.pin['b1']).put()
        nazca.Pin('b4', pin=mmi3c.pin['b0']).put()
        nazca.Pin('b5', pin=mmi3c.pin['b1']).put()
        nazca.Pin('b6', pin=mmi3d.pin['b0']).put()
        nazca.Pin('b7', pin=mmi3d.pin['b1']).put()

    return splitter_1x8

def Example_7():

    FUNC_NAME = ".Example_7()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        split = splitter_1by8('splitter').put(0)

        # The Nazca hierarchy is extendable as much as you like, e.g. a hierarchy of cells A, B and C like A({B[C, C]}, 
        # {B[C, C]}) could look like something in the image below, where each rectangle represents a cell and the bottom-left 
        # corner of each rectangle the origin (0, 0) of the cell.

        split2 = splitter_1by8('splitter 2').put(100, 800, -20)

        split3 = splitter_1by8('splitter 3').put(1400, 400, 20)

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def dbr_laser(Ldbr1=50, Ldbr2=500, Lsoa=750, Lpm=70):
    """Create a parametrized dbr laser building block."""
    with nazca.Cell(name='laser') as laser:
        #create an isolation cell for reuse
        iso = demo.isolation_act(length=20)

        #draw the laser
        s2a   = demo.s2a().put(0)
        dbr1  = demo.dbr(length=Ldbr1).put()
        iso.put()
        soa   = demo.soa(length=Lsoa).put()
        iso.put()
        phase = demo.phase_shifter(length=Lpm).put()
        iso.put()
        dbr2  = demo.dbr(length=Ldbr2).put()
        a2s   = demo.a2s().put()

        # add pins to the laser building block
        nazca.Pin('a0', pin=s2a.pin['a0']).put()
        nazca.Pin('b0', pin=a2s.pin['b0']).put()
        nazca.Pin('c0', pin=dbr1.pin['c0']).put()
        nazca.Pin('c1', pin=soa.pin['c0']).put()
        nazca.Pin('c2', pin=phase.pin['c0']).put()
        nazca.Pin('c3', pin=dbr2.pin['c0']).put()
    return laser

def Example_8():
    # place several laser structures in a file

    FUNC_NAME = ".Example_8()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #place several lasers:
        laser1 = dbr_laser(Lsoa=750).put(0)
        laser2 = dbr_laser(Lsoa=1000).put(0, -300)
        laser3 = dbr_laser(Lsoa=500, Ldbr1=20, Ldbr2=800, Lpm=150).put(0, -600)

        demo.shallow.bend(angle=-45).put(laser1.pin['b0'])

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def Example_9():
    # To make life easy, the DBR laser has been already defined in the demofab PDK, hence, a shorter way work with 
    # lasers is shown below. Here we create a number of laser building blocks, put them in a list and loop over them 
    # in a pythonic way to connect electrical bonding pads to each laser. Note that the core idea in Nazca is to create 
    # your building blocks, like the laser, verify them and use these blocks to simplify your main layout design.

    FUNC_NAME = ".Example_9()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        laser1 = demo.dbr_laser(Lsoa=750)
        laser2 = demo.dbr_laser(Lsoa=1000)
        laser3 = demo.dbr_laser(Lsoa=500, Ldbr1=20, Ldbr2=800, Lpm=150)
        laserBBs = [laser1, laser2, laser3]

        for j, laser in enumerate(laserBBs):
            demo.shallow.strt(length=100).put(0, 800*j)
            las = laser.put()
            demo.shallow.strt(length=200).put()

            for i, pinname in enumerate(['c0', 'c1', 'c2', 'c3']):
                pad = demo.pad_dc().put(las.pin['a0'].move(-i*250-150, -600, -90))
                demo.metaldc.sbend_p2p(las.pin[pinname], pad.pin['c0'], Lstart=(i+1)*75).put()

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def mzi(length=1000):
    with nazca.Cell(name='mzi') as mziBB:
        eopm = demo.eopm_dc(length=length, pads=True, sep=40)

        #part 1: place foundry blocks:
        mmi_left  = demo.mmi2x2_dp().put()
        eopm_top  = eopm.put(mmi_left.pin['b0'].move(135, 50))
        eopm_bot  = eopm.put(mmi_left.pin['b1'].move(135, -50), flip=True)
        mmi_right = demo.mmi2x2_dp().put(eopm_top.pin['b0'].move(135, -50))

        #part 2: add waveguide interconnects
        demo.deep.sbend_p2p(mmi_left.pin['b0'], eopm_top.pin['a0']).put()
        demo.deep.sbend_p2p(eopm_top.pin['b0'], mmi_right.pin['a0']).put()
        demo.deep.sbend_p2p(mmi_left.pin['b1'], eopm_bot.pin['a0']).put()
        demo.deep.sbend_p2p(eopm_bot.pin['b0'], mmi_right.pin['a1']).put()

        #part 3: add pins
        nazca.Pin('a0', pin=mmi_left.pin['a0']).put()
        nazca.Pin('a1', pin=mmi_left.pin['a1']).put()
        nazca.Pin('b0', pin=mmi_right.pin['b0']).put()
        nazca.Pin('b1', pin=mmi_right.pin['b1']).put()
        nazca.Pin('c0', pin=eopm_top.pin['c0']).put()
        nazca.Pin('c1', pin=eopm_top.pin['c1']).put()
        nazca.Pin('d0', pin=eopm_bot.pin['c0']).put()
        nazca.Pin('d1', pin=eopm_bot.pin['c1']).put()

    return mziBB

def Example_10():
    # layout of a defined MZM structure

    FUNC_NAME = ".Example_10()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        mzi(length=1000).put()
        mzi(length=500).put()

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)    

def Example_11():
    # layout of a defined MZM structure using the demofab devices

    FUNC_NAME = ".Example_11()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        mzi1 = demo.mzi(length=1000, sep=100).put(0)

        demo.deep.sbend(offset=500).put(mzi1.pin['b0'])
        mzi2a = demo.mzi(length=500, sep=200).put()

        demo.deep.sbend(offset=-500).put(mzi1.pin['b1'])
        mzi2b = demo.mzi(length=500, sep=200).put()

        nazca.export_gds()
    except Exception:
        print(ERR_STATEMENT)

def Example_12():
    # layout of a defined MZM structure using the demofab devices

    FUNC_NAME = ".Example_12()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        message = "Nazca, open source Photonic IC design in Python 3!"
        for i in range(7):
            T1 = nazca.text(text=message, height=70*0.85**i)
            T1.put(0, -i*100)
            T1.put(0, -1200+i*100)

            T2 = nazca.text(text=message, height=70*0.85**i, align='rb')
            T2.put(4000, -i*100)
            T2.put(4000, -1200+i*100)

        nazca.text('NAZCA', height=500, align='cc', layer=2).put(0.5*4000, -600)

        nazca.nazca_logo().put() # Nazca logo

        nazca.export_gds()
        
    except Exception:
        print(ERR_STATEMENT)
