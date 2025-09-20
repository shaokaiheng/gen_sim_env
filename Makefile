export OUT_SIM_DIR = /home/master/workarea/std_cell/sim/sim_clkdiv
export IN_RTL_DIR1 = /home/master/workarea/std_cell/src  #root folder  NO '/' at str-end

create_out_dir:
	@if [ ! -d $(OUT_SIM_DIR) ]; then \
		echo "Directory input_file does not exist, creating..."; \
		mkdir -p $(OUT_SIM_DIR); \
	fi


run_scr:
	python3 gen_sim_env.py $(OUT_SIM_DIR) $(IN_RTL_DIR1) | tee -i run.log

run:create_out_dir run_scr
