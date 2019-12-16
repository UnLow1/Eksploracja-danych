FOR /L %%A IN (1,1,166) DO (
  python main.py %%A > logs/result_%%A.txt
)