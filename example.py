from _opencv import ffi, lib


ESCAPE = ord("\x1b")


def fourcc((a, b, c, d)):
    """
    Calculate a FourCC integer from the four characters.

    http://www.fourcc.org/

    """

    return (((((ord(d) << 8) | ord(c)) << 8) | ord(b)) << 8) | ord(a);


capture = lib.cvCreateCameraCapture(0)
size = lib.cvSize(
    int(lib.cvGetCaptureProperty(capture, lib.CV_CAP_PROP_FRAME_WIDTH)),
    int(lib.cvGetCaptureProperty(capture, lib.CV_CAP_PROP_FRAME_HEIGHT)),
)

writer = lib.cvCreateVideoWriter(
    "/Users/Julian/Desktop/testing123.mpeg",
    fourcc("PIM1"),
    30,
    size,
    1,
)


lib.cvNamedWindow("Example", lib.CV_WINDOW_AUTOSIZE)


def escape_is_not_pressed(milliseconds=20):
    return lib.cvWaitKey(milliseconds) != ESCAPE


cascade = lib.cvLoadHaarClassifierCascade(
    "/Users/Julian/Desktop/haarcascades/haarcascade_frontalface_default.xml",
    lib.cvSize(1, 1),
)

storage = lib.cvCreateMemStorage(0)


while escape_is_not_pressed():
    frame = lib.cvQueryFrame(capture)
    objects = lib.cvHaarDetectObjects(
        frame,
        cascade,
        storage,
        1.1,
        3,
        0,
        lib.cvSize(0, 0),
        lib.cvSize(0, 0),
    )
    for i in xrange(objects.total):
        rectangle = ffi.cast("CvRect*", lib.cvGetSeqElem(objects, i))

        top_point = ffi.new("CvPoint *", [rectangle.x, rectangle.y])
        bottom_point = ffi.new(
            "CvPoint *",
            [rectangle.x + rectangle.width, rectangle.y + rectangle.height],
        )

        lib.cvRectangle(
            frame,
            top_point[0],
            bottom_point[0],
            lib.cvScalar(255, 0, 0, 0),
            1,
            8,
            0,
        )

    lib.cvWriteFrame(writer, frame)
    lib.cvShowImage("Example", frame)


lib.cvDestroyWindow("Example");
