#include "Server.hpp"
#include <cstring>

int main(int argc, char **argv)
{
    Server server;
    if (argc > 1) {
        char* databaseName = argv[1];
        if (strcmp(databaseName, "email_txt") == 0) {
            server.file_prefix_path = "/data/ls/data_config_file/email_txt/";
            server.audit_block_index_path = "/data/ls/data_config_file/log/audit_block_index_email_txt";
        }
        else if (strcmp(databaseName, "img_m") == 0) {
            server.file_prefix_path = "/data/ls/data_config_file/img_m/";
            server.audit_block_index_path = "/data/ls/data_config_file/log/audit_block_index_img_m";
        }
        else if (strcmp(databaseName, "img_million") == 0) {
            server.file_prefix_path = "/data/ls/data_config_file/img_txt/img_million/";
            server.audit_block_index_path = "/data/ls/data_config_file/log/audit_block_index_img_million";
        }
        else if (strcmp(databaseName, "text") == 0) {
            server.file_prefix_path = "/data/ls/data_config_file/img_txt/text/";
            server.audit_block_index_path = "/data/ls/data_config_file/log/audit_block_index_text";
        }
        // else if (databaseName == "search_result") {
        //     server.file_prefix_path = "/data/ls/data_config_file/search/";
        //     server.server_output_path = "/root/porla/porla/porla/porla/Server/data_server_output";
        //     server.initialize();
        //     return 0;
        else {
            server.file_prefix_path = "/data/ls/data_config_file/img_txt/text/";
            server.audit_block_index_path = "/data/ls/data_config_file/log/audit_block_index_text";
        }
    } 
    else {
        server.file_prefix_path = "/data/ls/data_config_file/img_txt/text/";
        server.audit_block_index_path = "/data/ls/data_config_file/log/audit_block_index_text";
    }
    // server.file_prefix_path = "/data/ls/data_config_file/test1GB/";
    server.server_output_path = "/data/ls/data_config_file/log/data_server_output";
    // server.initialize(); 
    server.Initialize_no_data();
    server.loadConfig();
    server.self_test();

    return 0;
}


