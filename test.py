raise NotImplementedError("Tests aren't formalized yet")

# Some intial ideas for testing below
# http://click.pocoo.org/5/testing/#basic-testing

# execture with resurrect path to temp dir
# assert custom path is useod
# http://click.pocoo.org/5/testing/#file-system-isolation
#
# Hypothesis: generate a large set of tmux_resurrect_{dt}.txt
#   dt-resolution -> seconds, no tz
# link last, assert last -> max(gen.dt)
# save state before clean
# clean, assert now-min(state) > threshold (if more than 10 files)
# assert all gen.dt > threshold in states
# assert archive temp dir is gone
# unpack/extract archive, assert all gen.dt in files
#
# delete all,
# generate 10/threshold n files,
# clean, assert unchanged
# link, assert latest
# link again, assert unchanged/aborted/error
