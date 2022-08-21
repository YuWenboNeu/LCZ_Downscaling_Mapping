import arcpy

in_raster = r"#"
out_folder=r"#"
out_base_name = "Basename"
split_method = "SIZE_OF_TILE"
format = "TIFF"
resampling_type="NEAREST"
tile_size = "32 32"
overlap = 0
units = "PIXELS"
arcpy.management.SplitRaster(in_raster, out_folder, out_base_name, split_method, format, resampling_type, "#", tile_size, overlap, units)
