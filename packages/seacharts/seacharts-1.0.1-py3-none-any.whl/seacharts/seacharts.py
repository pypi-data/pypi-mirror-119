from typing import List, Optional, Tuple, Union, Any

import matplotlib

import seacharts.display as dis
import seacharts.environment as env


class ENC:
    """Electronic Navigational Charts

    Reads and extracts features from a user-specified region of spatial data
    given in Cartesian coordinates. Based on Matplotlib, Shapely and Cartopy.
    An independent visualization window may be spawned and displayed using the
    multiprocessing option. Geometric shapes may be accessed through the
    attributes 'land', 'shore', and 'seabed'.

    :param size: tuple(width, height) of bounding box size
    :param origin: tuple(easting, northing) box origin of coordinates
    :param center: tuple(easting, northing) box center of coordinates
    :param buffer: int of dilation or erosion distance for geometries
    :param tolerance: int of maximum tolerance distance for geometries
    :param layers: list(str...) of feature layers to load or show
    :param depths: list(int...) of depth bins for feature layers
    :param files: list(str...) of file names for zipped FGDB files
    :param new_data: bool indicating if new files should be parsed
    :param border: bool for showing a border around the environment plot
    :param verbose: bool for status printing during geometry processing
    :param multiprocessing: bool for independent visualization display
    """

    def __init__(self,
                 size: Tuple[int, int] = None,
                 origin: Tuple[int, int] = None,
                 center: Tuple[int, int] = None,
                 buffer: Optional[int] = None,
                 tolerance: Optional[int] = None,
                 layers: Optional[List[str]] = None,
                 depths: Optional[List[int]] = None,
                 files: Optional[List[str]] = None,
                 new_data: Optional[bool] = None,
                 raw_data: Optional[bool] = None,
                 border: Optional[bool] = None,
                 verbose: Optional[bool] = None,
                 multiprocessing: bool = False,
                 ):
        matplotlib.use('TkAgg')
        if multiprocessing:
            dis.Display.init_multiprocessing()
            return
        self._environment = env.Environment(
            size, origin, center, buffer, tolerance, layers, depths, files,
            new_data, raw_data, border, verbose,
        )
        self.land = self._environment.topography.land
        self.shore = self._environment.topography.shore
        self.seabed = self._environment.hydrography.bathymetry
        self._display = dis.Display(self._environment)

    @property
    def supported_crs(self) -> str:
        """Return the supported coordinate reference system."""
        return self._environment.supported_crs

    @property
    def supported_layers(self) -> str:
        """Return the supported feature layers."""
        return self._environment.supported_layers

    def fullscreen_mode(self, arg: bool = True):
        """
        Enable or disable fullscreen mode view of environment figure.
        :param arg: boolean switching fullscreen mode on or off
        :return: None
        """
        self._display.toggle_fullscreen(arg)

    def colorbar(self, arg: bool = True):
        """
        Enable or disable the colorbar legend of environment figure.
        :param arg: boolean switching the colorbar on or off
        :return: None
        """
        self._display.toggle_colorbar(arg)

    def dark_mode(self, arg: bool = True):
        """
        Enable or disable dark mode view of environment figure.
        :param arg: boolean switching dark mode on or off
        :return: None
        """
        self._display.toggle_dark_mode(arg)

    def add_vessels(self, *args: Tuple[int, int, int, int, str]) -> None:
        """
        Add colored vessel features to the displayed environment plot.
        :param args: tuples with id, easting, northing, heading, color
        :return: None
        """
        self._display.refresh_vessels(list(args))

    def clear_vessels(self) -> None:
        """
        Remove all vessel features from the environment plot.
        :return: None
        """
        self._display.refresh_vessels([])

    def add_ownship(self,
                    easting: int,
                    northing: int,
                    heading: float,
                    hull_scale: float = 1.0,
                    lon_scale: float = 10.0,
                    lat_scale: float = 10.0,
                    ):
        """
        Add the body of a controllable vessel to the environment.
        :param easting: int denoting the ownship X coordinate
        :param northing: int denoting the ownship Y coordinate
        :param heading: float denoting the ownship heading in degrees
        :param hull_scale: optional float scaling the ownship body size
        :param lon_scale: optional float scaling the longitudinal horizon
        :param lat_scale: optional float scaling the lateral horizon
        :return: None
        """
        self._environment.create_ownship(
            easting, northing, heading, hull_scale, lon_scale, lat_scale
        )
        self._display.update_plot()

    def remove_ownship(self):
        """
        Remove the controllable vessel from the environment.
        :return: None
        """
        self._environment.ownship = None

    def add_hazards(self, depth: int, buffer: int = 0) -> None:
        """
        Add hazardous areas the environment, filtered by given depth.
        :param depth: int denoting the filter depth
        :param buffer: optional int denoting the buffer distance
        :return: None
        """
        self._environment.filter_hazardous_areas(depth, buffer)

    def draw_arrow(self,
                   start: Tuple[float, float],
                   end: Tuple[float, float],
                   color: str,
                   width: float = None,
                   head_size: float = None,
                   thickness: float = None,
                   edge_style: Union[str, tuple] = None,
                   ):
        """
        Add a straight arrow overlay to the environment plot.
        :param start: tuple of start point coordinate pair
        :param end: tuple of end point coordinate pair
        :param color: str of line color
        :param width: float denoting the line buffer width
        :param thickness: float denoting the Matplotlib linewidth
        :param edge_style: str or tuple denoting the Matplotlib linestyle
        :param head_size: float of head size (length) in meters
        :return: None
        """
        self._display.features.add_arrow(
            start, end, color, width, head_size, thickness, edge_style
        )

    def draw_circle(self,
                    center: Tuple[float, float],
                    radius: float,
                    color: str,
                    fill: bool = True,
                    thickness: float = None,
                    edge_style: Union[str, tuple] = None,
                    ):
        """
        Add a circle or disk overlay to the environment plot.
        :param center: tuple of circle center coordinates
        :param radius: float of circle radius
        :param color: str of circle color
        :param fill: bool which toggles the interior disk color
        :param thickness: float denoting the Matplotlib linewidth
        :param edge_style: str or tuple denoting the Matplotlib linestyle
        :return: None
        """
        self._display.features.add_circle(
            center, radius, color, fill, thickness, edge_style
        )

    def draw_line(self,
                  points: List[Tuple[float, float]],
                  color: str,
                  width: float = None,
                  thickness: float = None,
                  edge_style: Union[str, tuple] = None,
                  ):
        """
        Add a straight line overlay to the environment plot.
        :param points: list of tuples of coordinate pairs
        :param color: str of line color
        :param width: float denoting the line buffer width
        :param thickness: float denoting the Matplotlib linewidth
        :param edge_style: str or tuple denoting the Matplotlib linestyle
        :return: None
        """
        self._display.features.add_line(
            points, color, width, thickness, edge_style
        )

    def draw_polygon(self,
                     geometry: Union[Any, List[Tuple[float, float]]],
                     color: str,
                     interiors: List[List[Tuple[float, float]]] = None,
                     fill: bool = True,
                     thickness: float = None,
                     edge_style: Union[str, tuple] = None,
                     ):
        """
        Add an arbitrary polygon shape overlay to the environment plot.
        :param geometry: Shapely geometry or list of exterior coordinates
        :param interiors: list of lists of interior polygon coordinates
        :param color: str of rectangle color
        :param fill: bool which toggles the interior shape color
        :param thickness: float denoting the Matplotlib linewidth
        :param edge_style: str or tuple denoting the Matplotlib linestyle
        :return: None
        """
        self._display.features.add_polygon(
            geometry, color, interiors, fill, thickness, edge_style
        )

    def draw_rectangle(self,
                       center: Tuple[float, float],
                       size: Tuple[float, float],
                       color: str,
                       rotation: float = 0.0,
                       fill: bool = True,
                       thickness: float = None,
                       edge_style: Union[str, tuple] = None,
                       ):
        """
        Add a rectangle or box overlay to the environment plot.
        :param center: tuple of rectangle center coordinates
        :param size: tuple of rectangle (width, height)
        :param color: str of rectangle color
        :param rotation: float denoting the rectangle rotation in degrees
        :param fill: bool which toggles the interior rectangle color
        :param thickness: float denoting the Matplotlib linewidth
        :param edge_style: str or tuple denoting the Matplotlib linestyle
        :return: None
        """
        self._display.features.add_rectangle(
            center, size, color, rotation, fill, thickness, edge_style
        )

    def show_display(self, duration: float = 0.0) -> None:
        """
        Show a Matplotlib display window of a maritime environment.
        :param duration: optional int for window pause duration
        :return: None
        """
        self._display.show(duration)

    def refresh_display(self) -> None:
        """
        Manually redraw the environment display window.
        :return: None
        """
        self._display.draw_plot()

    def close_display(self) -> None:
        """
        Close the environment display window and clear all vessels.
        :return: None
        """
        self._display.terminate()
        self.clear_vessels()

    def save_image(self,
                   name: str = None,
                   scale: float = 1.0,
                   extension: str = 'png',
                   ):
        """
        Save the environment plot as a .png image.
        :param name: optional str of file name
        :param scale: optional float scaling the image resolution
        :param extension: optional str of file extension name
        :return: None
        """
        self._display.save_figure(name, scale, extension)
