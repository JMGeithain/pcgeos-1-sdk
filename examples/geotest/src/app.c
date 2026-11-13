#include "pcgeos1.h"

static int test_state;
static const char *test_message = "Press Enter or click to test TEST.GTD.";
static const char test_data[] =
    "GTD1\r\n"
    "GEOTEST 0.2 FILE TEST\r\n"
    "This file was written and read by GeoWorks 1.x.\r\n";
static char read_back[sizeof(test_data)];

static void run_file_test(void) {
    int h, n, extra, i;
    test_state = 1;
    test_message = "Creating TEST.GTD (existing files are not overwritten)...";
    pcg_invalidate();

    h = file_create_new("TEST.GTD");
    if (h < 0) {
        test_state = -1;
        test_message = (h == -80)
            ? "TEST.GTD already exists. Remove it and try again."
            : "FileCreate failed. No existing file was overwritten.";
        pcg_invalidate();
        return;
    }

    n = file_write(h, test_data, (unsigned)(sizeof(test_data) - 1));
    if (n != (int)(sizeof(test_data) - 1)) {
        file_close(h);
        test_state = -1;
        test_message = "FileWrite failed or wrote a short record.";
        pcg_invalidate();
        return;
    }
    if (file_close(h) < 0) {
        test_state = -1;
        test_message = "FileClose after writing failed.";
        pcg_invalidate();
        return;
    }

    test_message = "Reopening TEST.GTD and checking its contents...";
    pcg_invalidate();
    h = file_open("TEST.GTD");
    if (h < 0) {
        test_state = -1;
        test_message = "FileOpen failed after successful creation.";
        pcg_invalidate();
        return;
    }

    n = file_read(h, read_back, (unsigned)(sizeof(test_data) - 1));
    if (n != (int)(sizeof(test_data) - 1)) {
        file_close(h);
        test_state = -1;
        test_message = "FileRead returned an unexpected byte count.";
        pcg_invalidate();
        return;
    }
    extra = file_read(h, read_back + sizeof(test_data) - 1, 1);
    if (extra != 0) {
        file_close(h);
        test_state = -1;
        test_message = "File length check failed (expected end of file).";
        pcg_invalidate();
        return;
    }
    if (file_close(h) < 0) {
        test_state = -1;
        test_message = "FileClose after reading failed.";
        pcg_invalidate();
        return;
    }

    for (i = 0; i < (int)(sizeof(test_data) - 1); ++i) {
        if (read_back[i] != test_data[i]) {
            test_state = -1;
            test_message = "Read-back comparison failed.";
            pcg_invalidate();
            return;
        }
    }
    test_state = 2;
    test_message = "SUCCESS: TEST.GTD written, reopened and verified byte-for-byte.";
    pcg_invalidate();
}

void app_init(void) {
    test_state = 0;
    test_message = "Press Enter or click to test TEST.GTD.";
}

void app_draw(void) {
    pcg_rect(0,0,499,299,PCG_COLOR_WHITE);
    pcg_text(20,24,PCG_COLOR_BLACK,"GEOTEST - GeoWorks 1.x");
    pcg_text(20,52,PCG_COLOR_DARK_GREY,"Experimental native file I/O test (0.2).");
    pcg_text(20,88,PCG_COLOR_BLUE,test_message);
    if (test_state == 2)
        pcg_text(20,116,PCG_COLOR_GREEN,"File services passed the in-program verification.");
    else if (test_state < 0)
        pcg_text(20,116,PCG_COLOR_RED,"The test stopped; inspect the message above.");
    pcg_text(20,260,PCG_COLOR_DARK_GREY,"Target: GeoWorks 1.2.8 German / PC-GEOS 1.x");
}

void app_click(void) {
    if (test_state != 1) run_file_test();
}

void app_key(void) {
    if ((pcg_key_char & 0xff) == PCG_KEY_ENTER) {
        if (test_state != 1) run_file_test();
        pcg_key_handled = 1;
    }
}
