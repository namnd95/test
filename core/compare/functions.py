import config
from result import Result


def compare_line_ignore_space(line, out, ans, compare_function, **kagrs):
    out = out.split()
    ans = ans.split()
    if len(out) != len(ans):
        return Result(score=0, verdict='Line %d length mismatch' % line)
    for i in xrange(len(out)):
        if compare_function(out[i], ans[i], **kargs):
            return Result(
                score=0,
                verdict='Line %d at %d output %s answer %s' %
                (line, i + 1, out[i], ans[i])
            )
    return None


def compare_ignore_space(output, answer, compare_function, **kargs):
    try:
        file_out = open(output, 'r')
        file_ans = open(answer, 'r')
        out = file_out.read().split('\n')
        ans = file_ans.read().split('\n')
        file_out.close()
        file_ans.close()
    except:
        return Result(score=0, verdict='No output found')
    if len(out) != len(ans):
        return Result(score=0, verdict='Lines mismatch')
    for i in xrange(len(out)):
        value = compare_line_ignore_space(
            i + 1, out[i], ans[i], compare_function
        )
        if value is not None:
            return value
    return Result(1, 'AC')


def equal(output, answer):
    return output == answer


def equal_with_epsilon(output, answer, epsilon=1e-6, **kargs):
    try:
        out = float(output)
        ans = float(answer)
    except:
        return 0

    return abs(out - ans) < epsilon


def word_ignore_space(output, answer, **kargs):
    return compare_ignore_space(output, answer, equal)
config.update(word_ignore_space)


def float_ignore_space(output, answer, **kargs):
    return compare_ignore_space(output, answer, equal_with_epsilon, **kargs)
config.update(float_ignore_space)
