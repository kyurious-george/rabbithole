# Add fitted lines from models to a plot, padded with NAs
  # Because we're going to do this over and over again, and because we need
  # line up with time/date despite NAs
# Inputs:
  # the model (mdl)
  # a data frame (data, default "chicago")
  # subset of rows to use for plotting (subset, default all)
    # Not used in the solutions, but helpful for debugging and/or zooming in
  # name or index number of the column with x values (xcol, default "date")
  # optional extra arguments to lines() (...)
# Output:
  # as lines()
# Presumes:
  # mdl is a model with a predict() method, taking an argument named "newdata"
    # This presumption does NOT hold for splines
  # data has column whose name matches the xcol argument
  # data has columns needed by mdl's predict() method
  # mdl's predict() method understasnds na.action=na.pass
  # mdl's predict() method understands type="response"
lines.mdl.NApadded <- function(mdl, data=chicago, subset=1:nrow(data),
                               xcol="date",
                               ...) {
    # Invoke predict() for mdl on data, using the fact that the default behavior
    # and tell predict to return NA for any
    # row of data where variables are missing, rather than omitting that row
      # Not all predict() methods recognizd the na.action argument, but
      # predict.lm(), predict.glm() and predict.gam() all do so
      # Note that fitted() does not do this!
    preds.padded.with.NAs <- predict(mdl,
                                     newdata=data[subset,],
                                     type="response",
                                     na.action=na.pass)
    lines(x=data[subset, xcol],
          y=preds.padded.with.NAs,
          ...)
}
