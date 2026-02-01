import sys
import os

def Mkfl_str():
    str_mkfl = '''
.PHONY: comp sim clean

#-------------------------------------------------------------------------------------------------------
comp:
	vcs \\
		-timescale=1ns/1ps +define+SIMULATION \\
		-full64 +vc +v2k -sverilog -debug_access+all \\
		-lca -kdb \\
		tb.v \\
		-f ./syn.f \\
		-f ./sim.f \\
		-top tb \\
		-l compile.log
#-------------------------------------------------------------------------------------------------------
sim:
	./simv -l sim.log
#-------------------------------------------------------------------------------------------------------
vcs:comp sim
#-------------------------------------------------------------------------------------------------------
verdi  :
	verdi tb.v -sverilog -f ./syn.f -f ./sim.f  -ssf tb.fsdb -top tb -kdb ./simv.kdb -autoalias -rcFile novas.rc &
#-------------------------------------------------------------------------------------------------------
clean  :
	 rm  -rf  csrc  simv*  vc_hdrs.h  ucli.key  urg* *.log  novas.conf novas_dump.log *.fsdb* verdiLog  64* DVEfiles *.vpd verdi_config_file
#-------------------------------------------------------------------------------------------------------
'''
    return str_mkfl

def tb_file_str():
    str_tb = '''
`timescale 1ns/1ps
module tb();

logic clk,rst_n;
initial clk=0; initial rst_n=0; initial begin #99;rst_n=1;end
always #1 clk=~clk;



initial begin



end


initial begin
#3ms;

$display("TIME OUT FAIL");
$finish;
end

initial begin
$fsdbDumpfile ("tb.fsdb");
$fsdbDumpvars (0,"tb");
end


endmodule
'''
    return str_tb


def GetAllVerilogFilePath(directory):
    """
    查找指定目录及其子目录中所有 .v 和 .sv 文件
    
    参数:
        directory (str): 要搜索的根目录路径
        
    返回:
        list: 包含所有找到的 .v 和 .sv 文件的完整路径列表
    """
    verilog_files = []
    
    # 遍历目录树
    for root, _, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名
            if file.endswith(('.v', '.sv')):
                # 构建完整文件路径并添加到结果列表
                full_path = os.path.join(root, file)
                verilog_files.append(full_path)
    
    return verilog_files

if __name__ == "__main__":
    OUT_SIM_DIR = sys.argv[1]
    IN_RTL_DIR1 = sys.argv[2]
    print(f'>> Generatting Env Dir is [{OUT_SIM_DIR}]')
    auto_gen_file = []

    makefile_str = Mkfl_str()
    makefile_path = OUT_SIM_DIR+'/Makefile'
    auto_gen_file.append(makefile_path)
    with open(makefile_path,'w')as file:
        file.write(makefile_str)


    syn_f_path = OUT_SIM_DIR+'/syn.f'
    auto_gen_file.append(syn_f_path)
    with open(syn_f_path,'w')as file:
        v_file_paths = GetAllVerilogFilePath(IN_RTL_DIR1)
        for l in v_file_paths:
            file.write(l+'\n')

    sim_f_path = OUT_SIM_DIR+'/sim.f'
    auto_gen_file.append(sim_f_path)
    with open(sim_f_path,'w')as file:
        file.write('./tb.v\n')

    tb_f_path  = OUT_SIM_DIR+'/tb.v'
    auto_gen_file.append(tb_f_path)
    with open(tb_f_path,'w')as file:
        file.write(tb_file_str())


    for file_auto in auto_gen_file:
        print(f'  >> auto file [{file_auto}]')
