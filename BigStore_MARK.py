import time
import sys

from BigStore_student import  process_scanner_data_DO_NOT_PROFILE  as process_scanner_data
from BigStore_student_original import  main_things_to_profile as main_things_to_profile_original
from BigStore_student import main_things_to_profile as main_things_to_profile_student


def markWarpFactor( warpFactor ):
    print(f"""
---------------------------------------------------------------------------------
The warp factor ( speed increase ) is {warpFactor:.0f}. Which is 
{warpFactor * 100:.0f}%. Your code is going {warpFactor:.0f} times faster than 
the original version.
-----------------------------------------------------------------------------
    """)

    if warpFactor <= 5:
        print(""" 
Your warp factor is less 5 which can happen by chance. So no real speed increase. 
You might be doing the right thing but you could be slowing your self down in another way. 
for example you might be not removing the old slow code. So you can still get marks but just 
nothing for the speed increase in code. If this persists make a peudo code entry. 
You are likely to get 0 marks for this. 😞 
        """)
        return
    if warpFactor <= 10:
        print(""" 
Your warp factor is less 10 which is good. This definily indicates you are on the right track.The warp factor can be
higher. So either this is a random effect( try running the program again ) or you have only a partial solution. 
this is likely to get between  4 and 7 marks 😀

            """)
        return

    if warpFactor <= 17:
        print(f""" 
Your warp factor is less 17 which is very good. Nick's solution did about this level. 
With a warp factor of {warpFactor:.0f}. You are likely to look at 7 ... 10 marks (the maxium) for this section. 😀🎉
            """)
        return

    if warpFactor > 17:
        print(f""" 
With a warp factor of {warpFactor:.0f}. Is stunning. You are likely to get 10 Marks + a bonus (if possible.) 
Remember your code should do this consistently as you might get a feak occurrence (try again a few times).
Well done 😇
    """)
#END OF FUNCTIONB
#–-----------------------------------------------------------


file_path = 'scanner_data.csv'  # Ensure this path is correct
transactions = process_scanner_data(file_path)

print("#Raw transactions length = ",  len(transactions ))
print("1. Running the original version on your Machine.(hang on this can be slow)")
orignalTime_start = time.perf_counter()
prod_report_org, daily_sales_org, customers_org =  main_things_to_profile_original(  transactions )
orignalTime_end = time.perf_counter()
elapsed_time_original =  orignalTime_end - orignalTime_start
print(f"1.1 The original function took {elapsed_time_original:.3f} seconds to execute.")

if elapsed_time_original == 0.0 :
    print("Something has broken the original time is zero- email Nick Dalton with your problem and code.")
    sys.exit(-1)

print("")
print("2. Let us try timing your after code. This should be less time consuming, but lets see.")

studentTime_start = time.perf_counter()
prod_report_st, daily_sales_st, customers_st = main_things_to_profile_student( transactions )
studentTime_ends = time.perf_counter()

elapsed_time_student  = studentTime_ends - studentTime_start

print(f"2.1 Your code took {elapsed_time_student:.3f} seconds to execute.")

warpFactor =  elapsed_time_original / elapsed_time_student

markWarpFactor( warpFactor )