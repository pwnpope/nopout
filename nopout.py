from binaryninja import *
from binaryninjaui import UIContext


class NopOut:
    def __init__(self, bv):
        self.bv = bv


    def functions(self) -> dict:
        return {func.name: [func.start, func.highest_address - func.lowest_address + 1] for func in self.bv.functions}


    def analyze_all_functions(self, functions_info):
        funcs_analyzed = {}
        for name, func_info in functions_info.items():
            funcs_analyzed[name] = self.find_xrefs(func_info[0], func_info[1])
        return funcs_analyzed


    def find_xrefs(self, function_start: int, length: int) -> dict:
        xrefs = self.bv.get_code_refs(function_start)
        xref_per_func = {}
        count = 0
        for xrefs in xrefs:
            count += 1

        xref_per_func[function_start] = [count, length]
        return xref_per_func


    def nop_out(self, function_name: str, address: int, length: int):
        nops = b"\x90" * length
        self.bv.write(address, nops)
        print(f"[+] nopped out {function_name} @ {address:#0x}")


    def nop_out_handler(self, functions):
        for (function, details) in functions.items(): 
            for info in details.items():
                if info[1][0] == 0:
                    self.nop_out(function, info[0], info[1][1])


if __name__ == "__main__":
    bv.update_analysis_and_wait()
    
    no = NopOut(bv)
    func_info = no.functions()
    analysis = no.analyze_all_functions(func_info)
    no.nop_out_handler(analysis)
