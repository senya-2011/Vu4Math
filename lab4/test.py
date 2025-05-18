import methodology.point_5
import file_reader

x_test = [2.92, 4.5, 5.44, 6, 6.5]
y_test = [7.9488, 7.6088, 6.0687, 4.8687, 3.5]

result = methodology.point_5.run_full_pipeline(x_test, y_test)
print("predictions: \n")
print(result["predictions"])
print("\nresults: \n")
print(result["results"])
print("\nbest: \n")
print(result["best"])
print("\nstats: \n")
print(result["stats"])

print(file_reader.read_xy_from_txt_filepath("test.txt"))
