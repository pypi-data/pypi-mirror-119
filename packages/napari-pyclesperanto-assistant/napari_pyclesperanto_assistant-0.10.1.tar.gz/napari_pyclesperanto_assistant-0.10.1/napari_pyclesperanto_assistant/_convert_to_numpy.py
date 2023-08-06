# This is a list of utility functions for dealing with image data in napari.
# todo: As those are not clEsperanto-specific, we may want to split them out
#       and ship a separate package

import numpy as np
from napari import Viewer
from typing_extensions import Annotated
from napari.layers import Image, Labels, Layer
LayerInput = Annotated[Layer, {"label": "Image"}]


def convert_to_numpy(layer : LayerInput) -> Layer:
    if isinstance(layer, Labels):
        return Labels(np.asarray(layer.data), name="np " + layer.name)
    else:
        return Image(np.asarray(layer.data), name="np " + layer.name)

def convert_image_to_labels(layer : Image) -> Layer:
    return Labels(np.asarray(layer.data).astype(int), name="Labels " + layer.name)

def convert_labels_to_image(layer : Labels) -> Layer:
    return Image(np.asarray(layer.data), name="Image " + layer.name)

def convert_to_2d_timelapse(layer : LayerInput) -> Layer:
    if isinstance(layer, Labels):
        return Labels(np.expand_dims(layer.data, axis=1), name="2d+t " + layer.name)
    else:
        return Image(np.expand_dims(layer.data, axis=1), name="2d+t " + layer.name)


def make_labels_editable(labels : Labels) -> Labels:
    return Labels(np.asarray(labels.data), name="np " + labels.name)


def reset_brightness_contrast(image: Image):
    image.contrast_limits = (image.data.min(), image.data.max())


def auto_brightness_contrast(image: Image, lower_percentile : float = 1, upper_percentile : float = 99):
    data = np.asarray(image.data)
    lp = np.percentile(data, lower_percentile)
    up = np.percentile(data, upper_percentile)
    image.contrast_limits = (lp, up)


def auto_brightness_contrast_all_images(napari_viewer : Viewer, lower_percentile : float = 1, upper_percentile : float = 99):
    for layer in napari_viewer.layers:
        if isinstance(layer, Image):
            data = np.asarray(layer.data)
            lp = np.percentile(data, lower_percentile)
            up = np.percentile(data, upper_percentile)
            layer.contrast_limits = (lp, up)
    napari_viewer.window.remove_dock_widget(auto_brightness_contrast_all_images.native)


def split_stack(image : Image, napari_viewer : Viewer, axis : int = 0):
    data = np.asarray(image.data)
    for i in range(data.shape[axis]):
        napari_viewer.add_image(data.take(i, axis), name=image.name + "[" + str(i) + "]")
    napari_viewer.window.remove_dock_widget(split_stack.native)


def set_voxel_size(image : LayerInput, voxel_width : float = 1, voxel_height : float = 1, voxel_depth : float = 1):
    image.scale = [voxel_depth, voxel_height, voxel_width]


def set_voxel_size_of_all_layers(napari_viewer : Viewer, voxel_width : float = 1, voxel_height : float = 1, voxel_depth : float = 1):
    for layer in napari_viewer.layers:
        layer.scale = [voxel_depth, voxel_height, voxel_width]
    napari_viewer.window.remove_dock_widget(set_voxel_size_of_all_layers.native)

