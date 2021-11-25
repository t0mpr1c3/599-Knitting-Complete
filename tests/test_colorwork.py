from knitting_machine.Machine_State import Machine_State, Yarn_Carrier, Needle, Pass_Direction
from knitting_machine.machine_operations import outhook, miss, rack
from knitting_machine.operation_sets import Carriage_Pass, Instruction_Type, Instruction_Parameters


def _add_carriage_pass(carriage_pass, carriage_passes, instructions):
    if len(carriage_pass.needles_to_instruction_parameters) > 0:
        carriage_passes.append(carriage_pass)
        instructions.extend(carriage_pass.write_instructions())


def _write_instructions(filename: str, instructions):
    with open(filename, "w") as file:
        file.writelines(instructions)


def _cast_on(tuck_carrier, close_carrier, start_needle=0, end_needle=8, double=False):
    machine_state = Machine_State()
    carriage_passes = []
    instructions = [";!knitout-2\n",
                    ";;Machine: SWG091N2\n",
                    ";;Gauge: 5\n",
                    ";;Width: 250\n",
                    ";;Carriers: 1 2 3 4 5 6 7 8 9 10\n",
                    ";;Position: Center\n"]
    tuck_lr = {}
    for n in range(end_needle - 1, start_needle, -2):
        needle = Needle(True, n)
        tuck_lr[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=tuck_carrier)
    _add_carriage_pass(Carriage_Pass(Instruction_Type.Tuck, Pass_Direction.Right_to_Left, tuck_lr, machine_state), carriage_passes, instructions)
    tuck_rl = {}
    for n in range(start_needle, end_needle, 2):
        needle = Needle(True, n)
        tuck_rl[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=tuck_carrier)
    _add_carriage_pass(Carriage_Pass(Instruction_Type.Tuck, Pass_Direction.Left_to_Right, tuck_rl, machine_state), carriage_passes, instructions)

    if double:
        tuck_lr = {}
        for n in range(end_needle - 1, start_needle, -2):
            needle = Needle(False, n)
            tuck_lr[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=tuck_carrier)
        _add_carriage_pass(Carriage_Pass(Instruction_Type.Tuck, Pass_Direction.Right_to_Left, tuck_lr, machine_state), carriage_passes, instructions)
        tuck_rl = {}
        for n in range(start_needle, end_needle, 2):
            needle = Needle(False, n)
            tuck_rl[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=tuck_carrier)
        _add_carriage_pass(Carriage_Pass(Instruction_Type.Tuck, Pass_Direction.Left_to_Right, tuck_rl, machine_state), carriage_passes, instructions)

    knits = {}
    for n in range(end_needle - 1, start_needle - 1, -1):
        needle = Needle(True, n)
        knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=close_carrier)
    _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, knits, machine_state), carriage_passes, instructions)
    knits = {}
    for n in range(start_needle, end_needle):
        needle = Needle(not double, n)  # if double, knit a round by going on the back loops
        knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=close_carrier)
    _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, knits, machine_state), carriage_passes, instructions)
    return carriage_passes, instructions, machine_state


def test_platting():
    c1 = Yarn_Carrier([3, 4])
    c2 = Yarn_Carrier([4, 3])
    carriage_passes, instructions, machine_state = _cast_on(Yarn_Carrier(3), Yarn_Carrier(4))
    for row in range(0, 8):
        knits = {}
        if row % 2 == 0:
            for n in range(7, 3, -1):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c1)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, knits, machine_state), carriage_passes, instructions)
            knits = {}
            for n in range(3, -1, -1):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c2)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, knits, machine_state), carriage_passes, instructions)
        else:
            for n in range(0, 4):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c2)
            for n in range(4, 8):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c1)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, knits, machine_state), carriage_passes, instructions)

    instructions.append(outhook(machine_state, c1))
    # instructions.append(outhook(machine_state, c2))

    _write_instructions("platting.k", instructions)


def test_standard():
    c1 = Yarn_Carrier(3)
    c2 = Yarn_Carrier(4)
    carriage_passes, instructions, machine_state = _cast_on(c1, c2, end_needle=6)
    for row in range(0, 5):
        knits = {}
        if row % 2 == 0:
            for n in range(5, 3, -1):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c1)
            for n in range(3, 1, -1):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c2)
            for n in range(1, -1, -1):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c1)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, knits, machine_state), carriage_passes, instructions)
        else:
            for n in range(0, 2):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c1)
            for n in range(2, 4):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c2)
            for n in range(4, 6):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c1)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, knits, machine_state), carriage_passes, instructions)

    instructions.append(outhook(machine_state, c1))
    instructions.append(outhook(machine_state, c2))

    _write_instructions("standard.k", instructions)


def test_intarsia_misses():
    c1 = Yarn_Carrier(3)
    c2 = Yarn_Carrier(4)
    carriage_passes, instructions, machine_state = _cast_on(c1, c2)
    for row in range(0, 8):
        knits = {}
        if row % 2 == 0:
            for n in range(7, 3, -1):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c1)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, knits, machine_state), carriage_passes, instructions)
            instructions.append(miss(Pass_Direction.Right_to_Left, Needle(False, 0), c1))  # miss to cross yarn
            knits = {}
            for n in range(3, -1, -1):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c2)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, knits, machine_state), carriage_passes, instructions)
        else:
            for n in range(0, 4):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c2)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, knits, machine_state), carriage_passes, instructions)
            instructions.append(miss(Pass_Direction.Left_to_Right, Needle(False, 19), c2))  # miss to cross yarn
            knits = {}
            for n in range(4, 8):
                needle = Needle(True, n)
                knits[needle] = Instruction_Parameters(needle, involved_loop=-1, carrier=c1)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, knits, machine_state), carriage_passes, instructions)

    instructions.append(outhook(machine_state, c1))
    instructions.append(outhook(machine_state, c2))

    _write_instructions("intarsia-miss.k", instructions)


def test_jacquard():
    c1 = Yarn_Carrier(3)
    c2 = Yarn_Carrier(4)
    carriage_passes, instructions, machine_state = _cast_on(c1, c2, double=True, end_needle=6)
    for row in range(0, 8):
        c1_knits = {}
        c2_knits = {}
        if row % 2 == 0:
            for n in range(5, 3, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c1_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c1)
                c2_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c2)
            for n in range(3, 1, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c1_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c1)
                c2_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c2)
            for n in range(1, -1, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c1_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c1)
                c2_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c2)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, c1_knits, machine_state), carriage_passes, instructions)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, c2_knits, machine_state), carriage_passes, instructions)
        else:
            for n in range(0, 2):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c1_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c1)
                c2_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c2)
            for n in range(2, 4):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c1_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c1)
                c2_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c2)
            for n in range(4, 6):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c1_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c1)
                c2_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c2)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, c1_knits, machine_state), carriage_passes, instructions)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, c2_knits, machine_state), carriage_passes, instructions)

    instructions.append(outhook(machine_state, c1))
    instructions.append(outhook(machine_state, c2))

    _write_instructions("jacquard.k", instructions)


def test_birdseye():
    c1 = Yarn_Carrier(3)
    c2 = Yarn_Carrier(4)
    carriage_passes, instructions, machine_state = _cast_on(c1, c2, double=True)
    instructions.append(rack(machine_state, .25))  # rack for all needle knitting
    for row in range(0, 3):
        c1_knits = {}
        c2_knits = {}
        if row % 2 == 0:
            for n in range(7, 3, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c1_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c1)
                if n % 2 == 1:
                    c1_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c1)
                else:
                    c2_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c2)
            for n in range(3, -1, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c2_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c2)
                if n % 2 == 1:
                    c1_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c1)
                else:
                    c2_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c2)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, c1_knits, machine_state), carriage_passes, instructions)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, c2_knits, machine_state), carriage_passes, instructions)
        else:
            for n in range(0, 4):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c2_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c2)
                if n % 2 == 0:
                    c1_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c1)
                else:
                    c2_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c2)
            for n in range(4, 8):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                c1_knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c1)
                if n % 2 == 0:
                    c1_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c1)
                else:
                    c2_knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c2)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, c1_knits, machine_state), carriage_passes, instructions)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, c2_knits, machine_state), carriage_passes, instructions)

    instructions.append(outhook(machine_state, c1))
    instructions.append(outhook(machine_state, c2))

    _write_instructions("birdseye.k", instructions)


def test_birdseye_3():
    c1 = Yarn_Carrier(3)
    c2 = Yarn_Carrier(4)
    c3 = Yarn_Carrier(5)
    carrier = [c1, c2, c3]
    carriage_passes, instructions, machine_state = _cast_on(c1, c2, double=True, end_needle=6)
    instructions.append(rack(machine_state, .25))  # rack for all needle knitting
    for row in range(0, 8):
        knits = [{}, {}, {}]
        if row % 2 == 0:
            for n in range(5, 3, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                knits[(row + n) % 3][back_needle] = Instruction_Parameters(
                    back_needle, involved_loop=-1, carrier=carrier[(row + n) % 3])
                knits[(row + 0) % 3][front_needle] = Instruction_Parameters(
                    front_needle, involved_loop=-1, carrier=carrier[(row + 0) % 3])
            for n in range(3, 1, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                knits[(row + n) % 3][back_needle] = Instruction_Parameters(
                    back_needle, involved_loop=-1, carrier=carrier[(row + n) % 3])
                knits[(row + 1) % 3][front_needle] = Instruction_Parameters(
                    front_needle, involved_loop=-1, carrier=carrier[(row + 1) % 3])
            for n in range(1, -1, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                knits[(row + n) % 3][back_needle] = Instruction_Parameters(
                    back_needle, involved_loop=-1, carrier=carrier[(row + n) % 3])
                knits[(row + 2) % 3][front_needle] = Instruction_Parameters(
                    front_needle, involved_loop=-1, carrier=carrier[(row + 2) % 3])
            for c in range(0, 3):
                _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, knits[c], machine_state),
                                   carriage_passes, instructions)
        else:
            for n in range(0, 2):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                knits[(row + n) % 3][back_needle] = Instruction_Parameters(
                    back_needle, involved_loop=-1, carrier=carrier[(row + n) % 3])
                knits[(row + 2) % 3][front_needle] = Instruction_Parameters(
                    front_needle, involved_loop=-1, carrier=carrier[(row + 2) % 3])
            for n in range(2, 4):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                knits[(row + n) % 3][back_needle] = Instruction_Parameters(
                    back_needle, involved_loop=-1, carrier=carrier[(row + n) % 3])
                knits[(row + 1) % 3][front_needle] = Instruction_Parameters(
                    front_needle, involved_loop=-1, carrier=carrier[(row + 1) % 3])
            for n in range(4, 6):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                knits[(row + n) % 3][back_needle] = Instruction_Parameters(
                    back_needle, involved_loop=-1, carrier=carrier[(row + n) % 3])
                knits[(row + 0) % 3][front_needle] = Instruction_Parameters(
                    front_needle, involved_loop=-1, carrier=carrier[(row + 0) % 3])
            for c in range(0, 3):
                _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, knits[c], machine_state),
                                   carriage_passes, instructions)
    for c in range(0, 3):
        instructions.append(outhook(machine_state, carrier[c]))

    _write_instructions("birdseye-3.k", instructions)


def test_double_jersey():
    c1 = Yarn_Carrier(3)
    carriage_passes, instructions, machine_state = _cast_on(c1, c1, double=True, end_needle=4   )
    instructions.append(rack(machine_state, -.75))  # rack for all needle knitting
    for row in range(0, 10):
        knits = {}
        if row % 2 == 0:
            for n in range(3, -1, -1):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c1)
                knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c1)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Right_to_Left, knits, machine_state), carriage_passes, instructions)
        else:
            for n in range(0, 4):
                front_needle = Needle(True, n)
                back_needle = Needle(False, n)
                knits[front_needle] = Instruction_Parameters(front_needle, involved_loop=-1, carrier=c1)
                knits[back_needle] = Instruction_Parameters(back_needle, involved_loop=-1, carrier=c1)
            _add_carriage_pass(Carriage_Pass(Instruction_Type.Knit, Pass_Direction.Left_to_Right, knits, machine_state), carriage_passes, instructions)

    instructions.append(outhook(machine_state, c1))

    _write_instructions("double-jersey.k", instructions)


if __name__ == "__main__":
    test_double_jersey()
    test_birdseye_3()
    test_birdseye()
    test_platting()
    test_intarsia_misses()
    test_jacquard()
    test_standard()
