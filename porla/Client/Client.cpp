#include "Client.hpp"
#include <cstring>

int main(int argc, char **argv)
{    
    Client client;

    // int num_data_blocks = 1024;

    if (argc > 1) {
        char* databaseName = argv[1];
        // !!!!!!记得改文件位置
        if (strcmp(databaseName, "email_txt") == 0)
        //5397752KB=5.14GB=1349438blocks
        //算成8GB=2097152blocks
            client.num_blocks = 2097152;
        else if (strcmp(databaseName, "img_m") == 0)
        //16595112KB=15.8GB=4148778blocks
        //算成16GB=4194304blocks
            client.num_blocks = 4194304;
        else if (strcmp(databaseName, "img_million") == 0)
        //17070508KB=16G=4267627blocks
        //算成4194304blocks
        // img_txt/img_million
            client.num_blocks = 4194304;
        else if (strcmp(databaseName, "text") == 0)
        //  img_txt/text 
        //24132KB=23MB=6033blocks
        //算成32MB=8192blocks
            client.num_blocks = 8192;
        // else if (databaseName == "search_result") {
        //     // client.num_blocks = atoi(argv[2]);
        //     client.client_output_path = "/root/porla/porla/porla/porla/Client/data_client_output";
        //     // client.my_initialize();
        //     // return 0;
        // } 
        else
            client.num_blocks = 8192;
    } else {
        client.num_blocks = 8192;
    }
    // client.num_blocks = 262144;
    client.client_output_path = "/data/ls/data_config_file/log/data_client_output";
    // client.my_initialize();
    client.initialize_no_data();
    // client.my_test();
    client.audit();
    return 0;
}



