import click


@click.command()
@click.argument('brainf_ck', type=click.File('r'))
@click.option('-o', nargs=1, type=click.File('w'))


def c_compiler(brainf_ck, o):

    bfck_dict = {
        ">": "++ptr;\n",
        "<": "--ptr;\n",
        "+": "++(*ptr);\n",
        "-": "--(*ptr);\n",
        ".": """printf("%c",(*ptr));\n""",
        ",": """scanf("%c",ptr);\n""",
        "[": """while(*ptr) {\n""",
        "]": "}\n",
    }

    c_init = """#include <stdio.h>
#include <stdlib.h>

int main(void) {
    char *tape = malloc(sizeof(char)*40000);
    char *ptr = &tape[0];
"""

    number_indentations = 1

    source = brainf_ck.read()
    for data in source:
        if data in bfck_dict:
            if data == "[":
                c_init = c_init + "\n" + ("\t" * number_indentations) + bfck_dict[data]
                number_indentations = number_indentations + 1
            elif data == "]":
                number_indentations = number_indentations - 1
                c_init = c_init + ("\t" * number_indentations) + bfck_dict[data] + "\n"
            else:
                c_init = c_init + ("\t" * number_indentations) + bfck_dict[data]


    c_init = c_init + """\tprintf("\\n");\n\treturn 0;\n}"""

    o.write(c_init)
    o.flush()


if __name__ == "__main__":
    op = c_compiler()
